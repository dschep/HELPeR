from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Button, HTML
from crispy_forms.bootstrap import FormActions, FieldWithButtons

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
    options = forms.CharField(widget=forms.HiddenInput())

    class Meta:
        model = AgentConfig
        fields = ['options']

    def __init__(self, *args, **kwargs):
        super(AgentConfigUpdateForm, self).__init__(*args, **kwargs)
        for key in self.instance.agent.USER_CONFIG_KEYS:
            self.fields[key] = forms.CharField(
                initial=self.instance.options.get(key))
        user_configured = all(map(self.instance.options.get, self.instance.agent.USER_CONFIG_KEYS))
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
            [FormActions(Submit('save', 'Save'))]
        ))

    def clean(self):
        cleaned_data = super(AgentConfigUpdateForm, self).clean()
        self.cleaned_data['options'] = {}
        for key in self.instance.agent.USER_CONFIG_KEYS:
            self.cleaned_data['options'][key] = cleaned_data.get(key, '')
        for key in self.instance.agent.ACTION_CONFIG_KEYS:
            if key in self.instance.options:
                self.cleaned_data['options'][key] = self.instance.options[key]



class TaskPairUpdateForm(forms.ModelForm):
    class Meta:
        model = TaskPair
        fields = ['enabled', 'cause_agent', 'cause_task', 'cause_options',
                  'effect_agent', 'effect_task', 'effect_options']
    helper = horizontal_bs3_layout_helper
