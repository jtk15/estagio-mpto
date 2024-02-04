from django.urls import path

from .views import (
    state_index, 
    state_by_id,
    city_index, 
    city_by_id,
    natural_person_index, 
    natural_person_by_id,
    
    legal_person_index, 
    legal_person_by_id,
    person_index, 
    person_by_id,
    package_container_index,
    package_container_by_id,
    package_container_log_trace
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
    path('legalpeople/<int:id>', legal_person_by_id),
    
    path('people/', person_index),
    path('people/<int:id>', person_by_id),
    
    path('packages/', package_container_index),
    path('packages/<int:id>', package_container_by_id),
     path('packages/<str:unique_identify>/log', package_container_log_trace),
]