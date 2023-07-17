from rest_framework.test import APITestCase
from . import models
from experiences.models import Experience
from django.test import TestCase

class TestAmenities(APITestCase):

    NAME = "Amenity Test"
    DESC = "Amenity Des"
    URL = "/api/v1/experiences/"

    def setUp(self):
        models.Experience.objects.create(
            name=self.NAME,
            description=self.DESC,
        )
