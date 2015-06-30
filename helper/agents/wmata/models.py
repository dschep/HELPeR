from django import forms

from helper.models import Agent
from . import tasks


class WmataAgent(Agent):
    """
    <p>
    Register as a WMATA developer at <a href="https://developer.wmata.com/signup/"
        target="_blank">https://developer.wmata.com/signup/</a>.
    Then create suscribe to the default tier at <a target="_blank"
        href="https://developer.wmata.com/Products">
        https://developer.wmata.com/Products</a>.
    Enter the Primary key below.
    </p>
    """
    user_config_options = {
        'api_key': forms.CharField(),
    }
    cause_tasks = {'rail_incident': tasks.rail_incident}
