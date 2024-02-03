from helpers import restfy

from tracker.serializers import (
    LegalPersonSerializer,
    PersonSerializer, 
    StateSerializer, 
    CitySerializer, 
    NaturalPersonSerializer
)


city_index, city_by_id = restfy.make_rest(CitySerializer)
state_index, state_by_id = restfy.make_rest(StateSerializer)

person_index, person_by_id = restfy.make_rest(
    PersonSerializer, allow_update=False, allow_create=False, allow_delete=False
)

natural_person_index, natural_person_by_id = restfy.make_rest(NaturalPersonSerializer)
legal_person_index, legal_person_by_id = restfy.make_rest(LegalPersonSerializer)

