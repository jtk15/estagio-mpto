import json

from django.http import HttpResponse
from django.db import transaction
from tracker.models import State, City

from tracker.serializers import StateSerializer, CitySerializer

from helpers import restfy

city_index, city_by_id = restfy.make_rest(CitySerializer)
state_index, state_by_id = restfy.make_rest(StateSerializer)
