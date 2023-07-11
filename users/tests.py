from django.test import TestCase
from .models import User


class UserTestCase(TestCase):
    def setUp(self):
        User.objects.create(name="lion")
        User.objects.create(name="cat")

    def test_user_get(self):
        lion = User.objects.get(name="lion")
        cat = User.objects.get(name="cat")
        self.assertEqual(lion)
        self.assertEqual(cat)
