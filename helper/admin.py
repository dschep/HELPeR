from django.contrib import admin

from .models import AgentConfig, TaskPair

admin.site.register(AgentConfig)
admin.site.register(TaskPair)
