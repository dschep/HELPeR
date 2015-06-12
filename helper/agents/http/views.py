from django.views.generic import View
from django.http import JsonResponse, HttpResponse

from helper.agents.utils import get_from_event_store, send_to_event_store


class TaskView(View):
    def get(self, request, task_pair):
        return JsonResponse(list(get_from_event_store(task_pair.id, 'effect')),
                            safe=False)
    def post(self, request, task_pair):
        send_to_event_store([request.POST.dict()], task_pair.id, 'cause')
        return HttpResponse(status=201)
