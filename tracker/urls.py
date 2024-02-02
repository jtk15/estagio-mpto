from django.urls import path

from .views import (
    state_index, 
    state_by_id,
    city_index, 
    city_by_id,
    natural_person_index, 
    natural_person_by_id,
    
    legal_person_index, 
    legal_person_by_id
)


urlpatterns = [
    path('states/', state_index),
    path('states/<int:id>', state_by_id),

    path('cities/', city_index),
    path('cities/<int:id>', city_by_id),

    path('cities/', state_index),
    path('cities/<int:id>', state_by_id),
    
    path('naturalpeople/', natural_person_index),
    path('naturalpeople/<int:id>', natural_person_by_id),
    
     path('legalpeople/', legal_person_index),
    path('legalpeople/<int:id>', legal_person_by_id)
]