from collections import OrderedDict
from importlib import import_module

from django.db import models
from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError
from django.contrib.postgres.fields import HStoreField

from celery import chain

from helper.utils.tasks import dmap
from helper.utils.dedup.tasks import dedup_effect_wrapper, create_dedup_event


class AgentConfig(models.Model):
    name = models.CharField(max_length=255, primary_key=True)
    options = HStoreField(null=True)

    def __str__(self):
        return self.name.rsplit('.', 1)[-1].capitalize()

    def get_absolute_url(self):
        return reverse('agent_config_detail', kwargs={'pk': self.pk})

    def clean(self):
        try:
            self.agent
        except (ImportError, ValueError):
            raise ValidationError(
                '"{}" is not a valid agent'.format(self.name))

    @property
    def agent(self):
        return Agent.registry[self.name]

    @property
    def configured(self):
        all_config_options = (list(self.agent.user_config_options.keys())
                              + list(self.agent.action_config_options.keys()))
        if not self.options:
            return not all_config_options
        return (set(all_config_options) <= set(self.options.keys()))


class TaskPair(models.Model):
    enabled = models.BooleanField(default=True)
    cause_agent = models.ForeignKey(AgentConfig,
                                    related_name='cause_task_pairs')
    cause_task = models.CharField(max_length=255)
    cause_options = HStoreField(null=True, blank=True)
    effect_agent = models.ForeignKey(AgentConfig,
                                     related_name='effect_task_pairs')
    effect_task = models.CharField(max_length=255)
    effect_options = HStoreField(null=True, blank=True)

    def __str__(self):
        return '{}:{} -> {}:{}'.format(
            self.cause_agent, self.cause_task,
            self.effect_agent, self.effect_task,
        )

    def get_absolute_url(self):
        return reverse('task_pair_detail', kwargs={'pk': self.id})

    def clean(self):
        try:
            self.cause
        except AttributeError:
            raise ValidationError('module "{}" has no task "{}"'.format(
                self.cause_agent.name + '.task', self.cause_task
            ))
        except ImportError:
            raise ValidationError('module "{}" does not exist'.format(
                self.cause_agent.name + '.task'
            ))
        try:
            self.effect
        except AttributeError:
            raise ValidationError('module "{}" has no task "{}"'.format(
                self.effect_agent.name + '.task', self.effect_task
            ))
        except ImportError:
            raise ValidationError('module "{}" does not exist'.format(
                self.effect_agent.name + '.task'
            ))

    @property
    def cause(self):
        return self.cause_agent.agent.cause_tasks[self.cause_task]

    @property
    def effect(self):
        return self.effect_agent.agent.effect_tasks[self.effect_task]

    @property
    def cause_view(self):
        return getattr(import_module(self.cause_agent.name + '.views'),
                       self.cause_task)

    @property
    def effect_view(self):
        return getattr(import_module(self.effect_agent.name + '.views'),
                       self.effect_task)

    @property
    def cause_name(self):
        return self.cause_task.replace('_', ' ').capitalize()

    @property
    def effect_name(self):
        return self.effect_task.replace('_', ' ').capitalize()

    @property
    def schedule(self):
        try:
            return self.cause.every
        except (AttributeError, ImportError):
            pass

    def run(self):
        cause_options = self.cause_agent.options or {}
        cause_options.update({k: v for k, v in self.cause_options.items()
                              if not k.startswith('_')})
        cause_options['task_pair_id'] = self.id
        effect_options = self.effect_agent.options or {}
        effect_options.update({k: v for k, v in self.effect_options.items()
                               if not k.startswith('_')})
        effect_options['task_pair_id'] = self.id

        cause = self.cause.s(**cause_options)

        if getattr(self.cause, 'dedup_key', None) is not None:
            effect = dedup_effect_wrapper.s(
                dedup_key=self.cause.dedup_key,
                task_pair_id=self.id,
                effect=self.effect.s(**effect_options),
            )
        else:
            effect = self.effect.s(**effect_options)

        return chain(cause, dmap.s(effect))()

    def populate_dedup_events(self):
        if getattr(self.cause, 'dedup_key', None) is not None:
            cause_options = self.cause_agent.options or {}
            cause_options.update({k: v for k, v in self.cause_options.items()
                                if not k.startswith('_')})
            cause_options['task_pair_id'] = self.id

            cause = self.cause.s(**cause_options)
            effect = create_dedup_event.s(task_pair_id=self.id,
                                        dedup_key=self.cause.dedup_key)
            return chain(cause, dmap.s(effect))()


class Event(models.Model):
    TASK_TYPE_CHOICES = [('cause',)*2, ('effect',)*2]
    task_pair = models.ForeignKey('TaskPair')
    task_type = models.CharField(max_length=255, choices=TASK_TYPE_CHOICES)
    data = HStoreField()
    created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{0.task_pair}::{0.task_type}'.format(self)


class DedupEvent(models.Model):
    """
    A simpler event type for when you just need to suppress duplicate
    events by a simple unique key. For example, any facbeook event might be
    stored for deduplication by it's FBID
    """
    task_pair = models.ForeignKey(TaskPair)
    key = models.TextField()
    created = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('task_pair', 'key')

    def __str__(self):
        return '{0.task_pair}::{0.key}'.format(self)


class AgentMeta(type):
    def __init__(cls, name, bases, dct):
        if not hasattr(cls, 'registry'):
            # this is the base class.  Create an empty registry
            cls.registry = OrderedDict()
        else:
            name = dct['__module__']
            if name.endswith('.models'):
                name = name[:-7]
            assert name not in cls.registry, \
                'Only define one Agent class per module!!!'
            cls.registry[name] = cls

        super(AgentMeta, cls).__init__(name, bases, dct)


class Agent(metaclass=AgentMeta):
    user_config_options = {}
    action_config_options = {}
    cause_tasks = {}
    effect_tasks = {}

    @classmethod
    def register(cls, klass):
        assert klass.__module__ not in cls.registry, \
            'Only define one Agent class per module!!!'
        cls.registry[klass.__module__] = klass
