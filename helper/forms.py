from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from .models import AgentConfig, TaskPair


horizontal_bs3_layout_helper = FormHelper()
horizontal_bs3_layout_helper.form_class = 'form-horizontal'
horizontal_bs3_layout_helper.label_class = 'col-md-2'
horizontal_bs3_layout_helper.field_class = 'col-md-8'
horizontal_bs3_layout_helper.add_input(Submit('submit', 'Save'))


class AgentConfigCreateForm(forms.ModelForm):
    #name = forms.ChoiceField(choices=)
    class Meta:
        model = AgentConfig
        fields = ['name', 'options']


class AgentConfigUpdateForm(forms.ModelForm):
    class Meta:
        model = AgentConfig
        fields = ['options']
    helper = horizontal_bs3_layout_helper


class TaskPairUpdateForm(forms.ModelForm):
    class Meta:
        model = TaskPair
        fields = ['enabled', 'effect_agent', 'cause_task', 'cause_options',
                  'effect_agent', 'effect_task', 'effect_options']
    helper = horizontal_bs3_layout_helper
