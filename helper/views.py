from importlib import import_module

from django.shortcuts import render, get_object_or_404
from django.views.generic import View
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.http import Http404, HttpResponseNotAllowed, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.core.urlresolvers import reverse, reverse_lazy

from stronghold.decorators import public

from .models import AgentConfig, TaskPair
from .forms import AgentConfigUpdateForm, AgentConfigCreateForm, TaskPairUpdateForm



class AgentConfigListView(ListView):
    model = AgentConfig


class AgentConfigDetailView(UpdateView):
    model = AgentConfig
    template_name_suffix = '_detail'
    form_class = AgentConfigUpdateForm

    def get_success_url(self):
        return self.object.get_absolute_url()


class AgentConfigDeleteView(DeleteView):
    model = AgentConfig
    success_url = reverse_lazy('agent_config_list')

class AgentConfigCreateView(CreateView):
    model = AgentConfig
    form_class = AgentConfigCreateForm


class TaskPairListView(ListView):
    model = TaskPair


class TaskPairDetailView(UpdateView):
    model = TaskPair
    template_name_suffix = '_detail'
    form_class = TaskPairUpdateForm

    def get_success_url(object):
        return reverse('task_pair_list')


def dispatch_agent_config_url(request, agent_config_id, view_name):
    agent_config = get_object_or_404(AgentConfig, pk=agent_config_id)
    if view_name not in getattr(
            agent_config.agent, 'CONFIG_ACTIONS', []):
        raise Http404
    try:
        view = agent_config.get_agent_view(view_name)
    except (AttributeError, ImportError):
        raise Http404
    else:
        return view.as_view()(request, agent_config)


@public
@csrf_exempt
def dispatch_task_pair_url(request, task_pair_id, secret):
    task_pair = get_object_or_404(TaskPair, id=task_pair_id)
    try:
        if request.method == 'POST':
            view = task_pair.cause_view
            assert task_pair.cause_options.get('secret') == secret
        elif request.method == 'GET':
            view = task_pair.effect_view
            assert task_pair.effect_options.get('secret') == secret
        else:
            return HttpResponseNotAllowed(['POST', 'GET'])
    except (AttributeError, ImportError):
        raise Http404
    except AssertionError:
        return HttpResponseForbidden()
    else:
        return view.as_view()(request, task_pair)
