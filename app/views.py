from django.views.generic import ListView
from .models import TrainDetails, CHOOSE_STATUS


class TrainDetailsListView(ListView):
    model = TrainDetails
    template_name = "index.html"
    context_object_name = "train_details_list"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["choose_status"] = CHOOSE_STATUS
        return context
