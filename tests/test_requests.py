import json
from engine.stats import DataThread
from rest_framework.test import APIClient
from rest_framework import status
from django.test import TestCase
from django.urls import reverse
import time

DataThread.start = lambda _: None


class RequestTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_request(self):
        url = reverse('domain-request')
        response = self.client.post(url, data=json.dumps(
            {"A": 3, "timestamp": int(time.time() * 1000)}), content_type='application/json')
        assert response.status_code == 200, 'Bad response code'
        DataThread()._do_update()

        response = self.client.get(f'{url}?period=60000')
        assert response.status_code == 200, 'Bad response code'
        assert response.content.decode('UTF-8') == '{"A": 3}', 'Bad outup'


        num = ord('A')
        for i in range(25):
            response = self.client.post(url, data=json.dumps(
                {f"{chr(num + i)}": i + 10, "timestamp": int(time.time() * 1000)}), content_type='application/json')


        DataThread()._do_update()
        response = self.client.get(f'{url}?period=60000')
        assert "A" not in response.content.decode('UTF-8'), 'Bad outup'

        response = self.client.get(f'{url}?period=50000')
        assert response.content.decode('UTF-8') == '"50000 not registered"'

