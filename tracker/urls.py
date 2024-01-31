from django.urls import path
from .views import state_index, state_by_id

urlpatterns = [
    path('states/', state_index),
    path('states/<int:id>', state_by_id)
]