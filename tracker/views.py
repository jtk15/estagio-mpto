import json
from django.http import HttpResponse, HttpResponseNotAllowed
from helpers import restfy
from tracker.models import PackageContainer

from tracker.serializers import (
    LegalPersonSerializer,
    LogTraceSerializer,
    PersonSerializer, 
    StateSerializer, 
    CitySerializer, 
    NaturalPersonSerializer,
    PackageContainerSerializer
)


city_index, city_by_id = restfy.make_rest(CitySerializer)
state_index, state_by_id = restfy.make_rest(StateSerializer)

person_index, person_by_id = restfy.make_rest(
    PersonSerializer, allow_update=False, allow_create=False, allow_delete=False
)

natural_person_index, natural_person_by_id = restfy.make_rest(NaturalPersonSerializer)
legal_person_index, legal_person_by_id = restfy.make_rest(LegalPersonSerializer)
peckage_container_index, peckage_container_by_id = restfy.make_rest(PackageContainerSerializer)

def package_container_log_trace_list(request, unique_identify):
   
   return HttpResponse(status=501)


def package_container_log_trace_register(request, unique_identify):
    
    status=200
    result = {}
    
    payload = json.loads(request.body)
    
    try:
    
        packege_container = PackageContainer.objects.get(unique_identify=unique_identify)
        
        log_trace = LogTraceSerializer.decode(payload)
        
        packege_container.logs.add(log_trace, bulk=False)
        
        result = {
            "packet_container": PackageContainerSerializer.encode(packege_container),
            "log_trace": LogTraceSerializer.encode(log_trace),
        }
        
        status=200 
    except PackageContainer.DoesNotExist:
        
        status=404
        result = {
            'Mensage': f'Unique identify {unique_identify} invalido'
        }
    except Exception as e:
        status=400
        result={
            'Err': str(e)
        }
   
    return HttpResponse(
        status=status,
        content_type='application/json',
        content=json.dumps(result)
    )


def package_container_log_trace(request, unique_identify):

    status=200
    response = None
    
    if request.method == 'GET':
        
        response = package_container_log_trace_list(request, unique_identify)
        
    elif request.method == 'POST':
        
        response = package_container_log_trace_register(request, unique_identify)
    else:
        
        return HttpResponseNotAllowed(permitted_methods=['GET', 'POST'])
    
    return response


