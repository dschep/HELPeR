from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Button, HTML
from crispy_forms.bootstrap import FormActions, FieldWithButtons

from .models import AgentConfig, TaskPair
from .agents import AGENTS


horizontal_bs3_layout_helper = FormHelper()
horizontal_bs3_layout_helper.form_class = 'form-horizontal'
horizontal_bs3_layout_helper.label_class = 'col-md-2'
horizontal_bs3_layout_helper.field_class = 'col-md-8'
horizontal_bs3_layout_helper.add_input(Submit('submit', 'Save'))


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



class TaskPairUpdateForm(forms.ModelForm):
    class Meta:
        model = TaskPair
        fields = ['enabled', 'cause_agent', 'cause_task', 'cause_options',
                  'effect_agent', 'effect_task', 'effect_options']
    helper = horizontal_bs3_layout_helper
