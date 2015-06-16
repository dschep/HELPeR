from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import RedirectView

from .views import (AgentConfigDetailView, AgentConfigListView,
                    AgentConfigDeleteView, AgentConfigCreateView,
                    TaskPairDetailView, TaskPairListView,
                    TaskPairWizard)


urlpatterns = [
    # redirect to tasks for now
    url(r'^$', RedirectView.as_view(pattern_name='task_pair_list',
                                    permanent=False), name='home'),

    # agentconfig generics
    url(r'^agent/?$',
        AgentConfigListView.as_view(),
        name='agent_config_list'),
    url(r'^agent/add/?$',
        AgentConfigCreateView.as_view(),
        name='agent_config_create'),
    url(r'^agent/(?P<pk>[a-zA-Z.]+)/?$',
        AgentConfigDetailView.as_view(),
        name='agent_config_detail'),
    url(r'^agent/(?P<pk>[a-zA-Z.]+)/delete/?$',
        AgentConfigDeleteView.as_view(),
        name='agent_config_delete'),
    # agentconfig custom view
    url(r'^agent/(?P<agent_config_id>[a-zA-Z.]+)/(?P<view_name>\w+)',
        'helper.views.dispatch_agent_config_url',
        name='dispatch_agent_config_url'),

    # taskpair generics
    url(r'^task/?$',
        TaskPairListView.as_view(),
        name='task_pair_list'),
    url(r'^task/add/?$',
        TaskPairWizard.as_view(),
        name='task_pair_create'),
    url(r'^task/(?P<pk>\d+)/?$',
        TaskPairDetailView.as_view(),
        name='task_pair_detail'),
    # taskpair custom url
    url(r'^task/(?P<task_pair_id>\d+)/(?P<secret>\w+)',
        'helper.views.dispatch_task_pair_url',
        name='dispatch_task_pair_url'),

    # auth endpoints
    url(r'^accounts/login/$', 'django.contrib.auth.views.login',
        {'template_name': 'login.html'}, name="login"),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout',
        {'next_page': '/'}, name="logout"),
]

if 'django.contrib.admin' in settings.INSTALLED_APPS:
 urlpatterns += [
    url(r'^admin/', include(admin.site.urls)),
 ]
