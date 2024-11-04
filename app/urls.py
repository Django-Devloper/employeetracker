"""
    To define url patterns
"""

from django.urls import path
from .views import TrainDetailsListView

urlpatterns = [path("", TrainDetailsListView.as_view(), name="train_details_list")]
