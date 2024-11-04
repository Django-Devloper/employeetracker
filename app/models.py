# models.py

from django.db import models
from django.db.models.signals import post_migrate
from django.dispatch import receiver
import random

CHOOSE_STATUS = (
    ("LATE", "LATE"),
    ("ON_TIME", "ON_TIME"),
    ("CANCELLED", "CANCELLED"),
    ("ARRIVED", "ARRIVED"),
)


class TrainDetails(models.Model):
    name = models.CharField(max_length=100)
    status = models.CharField(max_length=30, choices=CHOOSE_STATUS)

    def __str__(self):
        return self.name


"""
To create initial train objects . Note This is not recommended way to add objects. 
"""


@receiver(post_migrate)
def create_initial_trains(sender, **kwargs):
    if not TrainDetails.objects.exists():
        for train in range(1, 21):
            name = f"Train No .{train}"
            status = random.choice([status[0] for status in CHOOSE_STATUS])
            TrainDetails.objects.create(name=name, status=status)


