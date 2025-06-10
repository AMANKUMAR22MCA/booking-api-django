from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import FitnessClass

class FitnessClassTests(APITestCase):

    def test_create_class_successfully(self):
        data = {
            "name": "Zumba Evening",
            "start_time": "2025-06-15T18:00:00Z",
            "instructor": "Nina D'Souza",
            "total_slots": 5,
            "available_slots": 5
        }
        response = self.client.post("/classes/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], "Zumba Evening")

    def test_list_classes(self):
        FitnessClass.objects.create(
            name="Pilates AM",
            start_time="2025-06-20T08:00:00Z",
            instructor="Amit Sen",
            total_slots=10,
            available_slots=10
        )
        response = self.client.get("/classes/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_class_invalid_data(self):
        data = {
            "name": "",  # Invalid
            "start_time": "invalid-time",
            "instructor": "Amit",
            "total_slots": -1,
            "available_slots": 0
        }
        response = self.client.post("/classes/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
