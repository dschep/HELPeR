from importlib import import_module

from django import forms
from django.contrib.postgres.forms.hstore import HStoreField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Button, HTML, Fieldset
from crispy_forms.bootstrap import FormActions, FieldWithButtons, StrictButton

from .models import AgentConfig, TaskPair
from .agents import AGENTS


horizontal_bs3_layout_helper = FormHelper()
horizontal_bs3_layout_helper.form_class = 'form-horizontal'
horizontal_bs3_layout_helper.label_class = 'col-md-2'
horizontal_bs3_layout_helper.field_class = 'col-md-8'
horizontal_bs3_layout_helper.add_input(Submit('submit', 'Save'))

def format_task_name(task_name):
        return task_name.replace('_', ' ').capitalize()


class AgentConfigCreateForm(forms.ModelForm):
    name = forms.ChoiceField()

    def __init__(self, *args, **kwargs):
        super(AgentConfigCreateForm, self).__init__(*args, **kwargs)
        self.fields['name'].choices = [(a, a.split('.')[-1].capitalize())
                                      for a in AGENTS if a not in
                                       AgentConfig.objects.all().values_list('name', flat=True)]

    class Meta:
        model = AgentConfig
        fields = ['name']

    helper = FormHelper()

AgentConfigCreateForm.helper.form_class = 'form-horizontal'
AgentConfigCreateForm.helper.label_class = 'col-md-2 col-md-offset-2'
AgentConfigCreateForm.helper.field_class = 'col-md-2'
AgentConfigCreateForm.helper.add_input(Submit('submit', 'Add',
                                            css_class='btn-success'))


class AgentConfigUpdateForm(forms.ModelForm):
    options = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = AgentConfig
        fields = ['options']

    def __init__(self, *args, **kwargs):
        super(AgentConfigUpdateForm, self).__init__(*args, **kwargs)
        for key in self.instance.agent.USER_CONFIG_KEYS:
            self.fields[key] = forms.CharField()
            if self.instance.options:
                self.fields[key].initial=self.instance.options.get(key)
        if self.instance.options:
            user_configured = all(map(self.instance.options.get,
                                      self.instance.agent.USER_CONFIG_KEYS))
        else:
            user_configured = False
        if user_configured:
            for key in self.instance.agent.ACTION_CONFIG_KEYS:
                self.fields[key] = forms.CharField(
                    widget=forms.TextInput(attrs={'readonly':'readonly'}),
                    initial=self.instance.options.get(key))

        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-2'
        self.helper.field_class = 'col-md-8'
        self.helper.layout = Layout(*(
            self.instance.agent.USER_CONFIG_KEYS +
            (
            [FieldWithButtons(var, Button(
                var+'-action', 'Refresh', css_class='btn-success',
                onClick=("javascript:window.location.href+='/" + action +
                         "';")))
                for var, action in
             self.instance.agent.ACTION_CONFIG_KEYS.items()]
            if user_configured else []) +
            [FormActions(Submit('save', 'Save'),
                         Button('delete', 'Delete', css_class='btn-danger',
                                onClick=("javascript:window.location.href"
                                         "+='/delete'")
                                ))]
        ))

    def clean(self):
        cleaned_data = super(AgentConfigUpdateForm, self).clean()
        self.cleaned_data['options'] = {}
        for key in self.instance.agent.USER_CONFIG_KEYS:
            self.cleaned_data['options'][key] = cleaned_data.get(key, '')
        for key in self.instance.agent.ACTION_CONFIG_KEYS:
            if self.instance.options and key in self.instance.options:
                self.cleaned_data['options'][key] = self.instance.options[key]


def submit_buttons_from_choicefield(name, choicefield, prefix=None):
    name_fmt = '{prefix}-{name}' if prefix else '{name}'
    return [
        StrictButton(format_task_name(label), value=value, type='submit',
                     name=name_fmt.format(name=name, prefix=prefix))
        for value, label in choicefield.choices
    ]


class TaskPairChooseCauseAgentForm(forms.Form):
    cause_agent = forms.ModelChoiceField(queryset=AgentConfig.objects.all(),
                                         empty_label=None)
    def __init__(self, *args, **kwargs):
        super(TaskPairChooseCauseAgentForm, self).__init__(*args, **kwargs)
        self.fields['cause_agent'].queryset = AgentConfig.objects.filter(
            pk__in=[agent.pk for agent in AgentConfig.objects.all()
                    if len(agent.agent.CAUSE_TASKS) > 0]
        )
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(Fieldset(
            'Choose a Cause Agent',
            *submit_buttons_from_choicefield(
                'cause_agent', self.fields['cause_agent'], kwargs.get('prefix')
            )
        ))


class TaskPairChooseCauseTaskForm(TaskPairChooseCauseAgentForm):
    cause_agent = forms.ModelChoiceField(queryset=AgentConfig.objects.all(),
                                         widget=forms.HiddenInput())
    # agent isn't in initial when validating, just make sure it's a
    # task somewhere so it doesn't fail. user should only have selected
    # one from above, and it will be re-validated on the final save
    cause_task = forms.ChoiceField(choices=[
        (task, task) for agent_config in AgentConfig.objects.all()
        for task in agent_config.agent.CAUSE_TASKS])

    def __init__(self, *args, **kwargs):
        super(TaskPairChooseCauseTaskForm, self).__init__(*args, **kwargs)
        if 'cause_agent' in kwargs.get('initial', {}):
            self.fields['cause_task'].choices = [(t, t) for t in
                AgentConfig.objects.get(pk=kwargs['initial']['cause_agent']).agent.CAUSE_TASKS]
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(Fieldset(
            'Choose a Cause',
            'cause_agent',
            *submit_buttons_from_choicefield(
                'cause_task', self.fields['cause_task'], kwargs.get('prefix')
            )
        ))


class TaskPairCauseOptionsForm(TaskPairChooseCauseTaskForm):
    cause_task = forms.ChoiceField(choices=[
        (task, task) for agent_config in AgentConfig.objects.all()
        for task in agent_config.agent.CAUSE_TASKS],
        widget=forms.HiddenInput(),
    )
    cause_options = forms.CharField(required=False, widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        super(TaskPairCauseOptionsForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.label_class = 'col-md-2'
        self.helper.field_class = 'col-md-8'
        fields = ['cause_agent', 'cause_task']

        predefined_fields = {}
        for key in ['cause_agent', 'cause_task']:
            if key in kwargs.get('initial', {}):
                predefined_fields[key] = kwargs['initial'][key]
            elif 'prefix' in kwargs and '{}-{}'.format(kwargs['prefix'], key) in self.data:
                predefined_fields[key] = self.data['{}-{}'.format(kwargs['prefix'], key)]
            elif key in self.data:
                predefined_fields[key] = self.data[key]

        if set(['cause_agent', 'cause_task']) <= set(predefined_fields):
            tasks_module = import_module(predefined_fields['cause_agent'] +
                                         '.tasks')
            task = getattr(tasks_module, predefined_fields['cause_task'])
            if getattr(task, 'help', False):
                fields.append(HTML("""
                                <div class="alert alert-info" role="alert">
                                {help}
                                </div>
                                """.format(help=task.help)))
            for option in getattr(task, 'options', []):
                self.fields['cause-opt-'+option] = forms.CharField(
                    label=option)
                fields.append('cause-opt-'+option)
            if not getattr(task, 'options', False):
                fields.append(HTML("""
                                <div class="alert alert-success" role="alert">
                                No options to complete
                                </div>
                                """))
        fields.append(FormActions(Submit('submit', 'Continue')))
        self.helper.layout = Layout(Fieldset('Task Options', *fields))

    def clean(self):
        cleaned_data = super(TaskPairCauseOptionsForm, self).clean()
        cause_options = {k.split('-', 2)[2]: v for k, v in cleaned_data.items()
                         if k.startswith('cause-opt-')}
        cleaned_data['cause_options'] = cause_options
        cleaned_data = {k: v for k, v in cleaned_data.items()
                        if not k.startswith('cause-opt-')}
        return cleaned_data

class TaskPairChooseEffectAgentForm(TaskPairCauseOptionsForm):
    effect_agent = forms.ModelChoiceField(queryset=AgentConfig.objects.all(),
                                          empty_label=None)
    def __init__(self, *args, **kwargs):
        super(TaskPairChooseCauseAgentForm, self).__init__(*args, **kwargs)
        self.fields['effect_agent'].queryset = AgentConfig.objects.filter(
            pk__in=[agent.pk for agent in AgentConfig.objects.all()
                    if len(agent.agent.EFFECT_TASKS) > 0]
        )
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(Fieldset(
            'Choose a Effect Agent',
            'cause_agent', 'cause_task', 'cause_options',
            *submit_buttons_from_choicefield(
                'effect_agent', self.fields['effect_agent'], kwargs.get('prefix')
            )
        ))


class TaskPairChooseEffectTaskForm(TaskPairChooseEffectAgentForm):
    effect_agent = forms.ModelChoiceField(queryset=AgentConfig.objects.all(),
                                          widget=forms.HiddenInput())
    effect_task = forms.ChoiceField(choices=[
        (task, task) for agent_config in AgentConfig.objects.all()
        for task in agent_config.agent.EFFECT_TASKS])

    def __init__(self, *args, **kwargs):
        super(TaskPairChooseEffectTaskForm, self).__init__(*args, **kwargs)
        if 'effect_agent' in kwargs.get('initial', {}):
            self.fields['effect_task'].choices = [(t, t) for t in
                AgentConfig.objects.get(pk=kwargs['initial']['effect_agent']).agent.EFFECT_TASKS]
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(Fieldset(
            'Choose a Effect',
            'cause_agent', 'cause_task', 'cause_options', 'effect_agent',
            *submit_buttons_from_choicefield(
                'effect_task', self.fields['effect_task'], kwargs.get('prefix')
            )
        ))


class TaskPairEffectOptionsForm(TaskPairChooseEffectTaskForm):
    effect_task = forms.ChoiceField(choices=[
        (task, task) for agent_config in AgentConfig.objects.all()
        for task in agent_config.agent.EFFECT_TASKS],
        widget=forms.HiddenInput(),
    )
    effect_options = forms.CharField(required=False, widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        super(TaskPairEffectOptionsForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.label_class = 'col-md-2'
        self.helper.field_class = 'col-md-8'
        fields = ['cause_agent', 'cause_task', 'cause_options',
                  'effect_agent', 'effect_task']
        ## sometimes data is missing from initial but is in self.data..
        predefined_fields = {}
        for key in ['cause_agent', 'cause_task',
                    'effect_agent', 'effect_task']:
            if key in kwargs.get('initial', {}):
                predefined_fields[key] = kwargs['initial'][key]
                continue
            elif 'prefix' in kwargs and '{}-{}'.format(kwargs['prefix'], key) in self.data:
                    predefined_fields[key] = self.data['{}-{}'.format(kwargs['prefix'], key)]
                    continue
            elif key in self.data:
                predefined_fields[key] = self.data[key]

        if set(['cause_agent', 'cause_task']) <= set(predefined_fields):
            agent = AgentConfig.objects.get(pk=predefined_fields['cause_agent'])
            tasks_module = import_module(predefined_fields['cause_agent'] +
                                         '.tasks')
            task = getattr(tasks_module, predefined_fields['cause_task'])
            fields.append(HTML("""
                            <div class="alert alert-info" role="alert">
                               <p>
                                The <strong>{agent}</strong>:{task} Cause Task
                                makes the following keys
                                available for use in Effect options: {keys}
                               </p>
                               <p>
                               Use python3-style string formatting. IE:
                                <kbd>/var/log/{{{ex}}}/</kbd>
                               </p>
                            </div>
                            """.format(ex=('fs' if not task.event_keys
                                           else task.event_keys[0]),
                                       keys=', '.join(
                                           '<kbd>{}</kbd>'.format(key)
                                           for key in task.event_keys),
                                       agent=agent,
                                       task=format_task_name(
                                           predefined_fields['cause_task']),
                                       )))
        if set(['effect_agent', 'effect_task']) <= set(predefined_fields):
            tasks_module = import_module(predefined_fields['effect_agent'] +
                                         '.tasks')
            task = getattr(tasks_module, predefined_fields['effect_task'])
            if getattr(task, 'help', False):
                fields.append(HTML("""
                                <div class="alert alert-info" role="alert">
                                {help}
                                </div>
                                """.format(help=task.help)))
            for option in getattr(task, 'options', []):
                self.fields['effect-opt-'+option] = forms.CharField(
                    label=option)
                fields.append('effect-opt-'+option)
            if not getattr(task, 'options', False):
                fields.append(HTML("""
                                <div class="alert alert-success" role="alert">
                                No options to complete
                                </div>
                                """))
        fields.append(FormActions(Submit('submit', 'Continue')))
        self.helper.layout = Layout(Fieldset('Task Options', *fields))

    def clean(self):
        cleaned_data = super(TaskPairEffectOptionsForm, self).clean()
        effect_options = {k.split('-', 2)[2]: v for k, v in cleaned_data.items()
                          if k.startswith('effect-opt-')}
        cleaned_data['effect_options'] = effect_options
        cleaned_data = {k: v for k, v in cleaned_data.items()
                        if not k.startswith('effect-opt-')}
        return cleaned_data

class TaskPairUpdateForm(forms.ModelForm):
    cause_options = HStoreField(widget=forms.HiddenInput(), required=False)
    effect_options = HStoreField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = TaskPair
        fields = ['enabled', 'cause_options', 'effect_options']

    def __init__(self, *args, **kwargs):
        super(TaskPairUpdateForm, self).__init__(*args, **kwargs)

        # uh.. do nothing fancy if these aren't set for some reason
        if 'instance' not in kwargs:
            return

        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-2'
        self.helper.field_class = 'col-md-8'

        cause_fields = []
        if getattr(self.instance.cause, 'help', False):
            cause_fields.append(HTML("""
                            <div class="alert alert-info" role="alert">
                            {help}
                            </div>
                            """.format(help=self.instance.cause.help)))
        for option in getattr(self.instance.cause, 'options', []):
            self.fields['cause-opt-'+option] = forms.CharField(
                label=option,
                initial=self.instance.cause_options.get(option),
            )
            cause_fields.append('cause-opt-'+option)
        if not getattr(self.instance.cause, 'options', False):
            cause_fields.append(HTML("""
                            <div class="alert alert-success" role="alert">
                            No options to complete
                            </div>
                            """))
        effect_fields = []
        effect_fields.append(HTML("""
                        <div class="alert alert-info" role="alert">
                            <p>
                            The Cause Task makes the following keys
                            available for use in Effect options: {keys}
                            </p>
                            <p>
                            Use python3-style string formatting. IE:
                            <kbd>/var/log/{{{ex}}}/</kbd>
                            </p>
                        </div>
                        """.format(ex=('fs' if not self.instance.cause.event_keys
                                        else self.instance.cause.event_keys[0]),
                                    keys=', '.join(
                                        '<kbd>{}</kbd>'.format(key)
                                        for key in self.instance.cause.event_keys),
                                    )))
        if getattr(self.instance.effect, 'help', False):
            effect_fields.append(HTML("""
                            <div class="alert alert-info" role="alert">
                            {help}
                            </div>
                            """.format(help=self.isntance.effect.help)))
        for option in getattr(self.instance.effect, 'options', []):
            self.fields['effect-opt-'+option] = forms.CharField(
                label=option,
                initial=self.instance.effect_options.get(option),
            )
            effect_fields.append('effect-opt-'+option)
        if not getattr(self.instance.effect, 'options', False):
            effect_fields.append(HTML("""
                            <div class="alert alert-success" role="alert">
                            No options to complete
                            </div>
                            """))

        self.helper.layout = Layout(
            Fieldset('Task Options', 'enabled'),
            Fieldset('<strong>{}</strong>:{}'.format(self.instance.cause_agent,
                                                     self.instance.cause_name),
                     *cause_fields),
            Fieldset('<strong>{}</strong>:{}'.format(self.instance.effect_agent,
                                                     self.instance.effect_name),
                     *effect_fields),
            FormActions(
                Submit('save', 'Save'),
                Button('delete', 'Delete', css_class='btn-danger',
                       onClick=("javascript:window.location.href+='/delete'"))
            ),
        )

    def clean(self):
        cleaned_data = super(TaskPairUpdateForm, self).clean()
        cleaned_data['cause_options'] = {
            k.split('-', 2)[2]: v for k, v in self.cleaned_data.items()
            if k.startswith('cause-opt-')
        }
        cleaned_data['effect_options'] = {
            k.split('-', 2)[2]: v for k, v in self.cleaned_data.items()
            if k.startswith('effect-opt-')
        }
        return cleaned_data
