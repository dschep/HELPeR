import requests
from celery import shared_task
from django import forms

from helper.scheduler import schedule
from helper.utils.dedup.decorators import dedup


@dedup('id')
@schedule(1)
@shared_task
def rail_incident(api_key, line, task_pair_id):
    resp = requests.get('https://api.wmata.com/Incidents.svc/json/Incidents',
                        headers={'api_key': api_key})
    resp.raise_for_status()

    events = []
    for incident in resp.json().get('Incidents', []):
        lines = [l.strip() for l in incident['LinesAffected'].split(';') if l.strip()]
        if line not in lines:
            continue
        events.append({
            'id': incident['IncidentID'],
            'lines': ','.join(lines),
            'description': incident['Description'],
            'date_updated': incident['DateUpdated'],
        })
    return events
rail_incident.event_keys = ['id', 'lines', 'description', 'date_updated']
rail_incident.options = {'line': forms.ChoiceField(label='Line', choices=[
    ('RD', 'Red'),
    ('GR', 'Green'),
    ('OR', 'Orange'),
    ('YL', 'Yellow'),
    ('BL', 'Blue'),
    ('SV', 'Silver'),
])}
