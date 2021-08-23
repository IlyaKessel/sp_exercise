from engine.stats import DataThread
from django.http.response import JsonResponse
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
import json

TIMES = settings.TIMES
ENTRIES_NUM = settings.ENTRIES_NUM

class DomainAPIView(ListCreateAPIView):
    def get(self, request, *args, **kwargs):
        period = self.request.GET.get('period', None)
        if period is None:
            return Response("No time period is provided", status=status.HTTP_400_BAD_REQUEST)
        period = int(period)
        if period not in TIMES:
            return Response(f"{period} not registered", status=status.HTTP_400_BAD_REQUEST)
        results = DataThread().get_maxes(period, ENTRIES_NUM)
        return JsonResponse(results)

    def post(self, request, *args, **kwargs):
        DataThread().add_events(request.data)
        return Response('Success', content_type='application/json')
