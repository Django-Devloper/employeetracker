# tests.py
from django.db.models.signals import post_migrate
from django.test import TestCase
from django.urls import reverse
from django.core.management import call_command
from .models import TrainDetails, CHOOSE_STATUS


class TrainDetailsModelTestCase(TestCase):
    def test_train_details_creation(self):
        # Test if TrainDetails objects are created properly
        TrainDetails.objects.create(name="Test Train", status="LATE")
        train = TrainDetails.objects.get(name="Test Train")
        self.assertEqual(train.status, "LATE")

    def test_create_initial_trains_signal(self):
        # Test the post_migrate signal to create initial trains
        call_command("migrate")  # Ensure migrations are up to date
        post_migrate.send(
            sender=self.__class__, app_config=TrainDetails._meta.app_config
        )
        self.assertTrue(TrainDetails.objects.exists())


class TrainDetailsListViewTestCase(TestCase):
    def setUp(self):
        # Create some sample TrainDetails objects for testing
        for train_num in range(1, 6):
            TrainDetails.objects.create(
                name=f"Test Train {train_num}", status="ON_TIME"
            )

    def test_train_details_list_view(self):
        # Test if TrainDetailsListView returns a valid response and contains the expected data
        response = self.client.get(reverse("train_details_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")
        self.assertIn("train_details_list", response.context)

        # Compare the queryset against a list of expected values
        expected_values = list(TrainDetails.objects.all())
        actual_values = list(response.context["train_details_list"])
        self.assertEqual(expected_values, actual_values)

    def test_train_details_list_view_context(self):
        # Test if the context data is passed correctly to the template
        response = self.client.get(reverse("train_details_list"))
        self.assertIn("choose_status", response.context)
        self.assertEqual(response.context["choose_status"], CHOOSE_STATUS)
