import json
from django.http import HttpResponse
from django.db import transaction
from tracker.models import State
from tracker.serealization import StateSerialiazer


def state_list(request):
     
    query = State.objects.all()

    if query.exists():
        
        response = HttpResponse(
            content_type='application/json',
            content=json.dumps([
                StateSerialiazer.serealizer(state) for state in query
            ])
                
        )

        return response
    else:
        
        response = HttpResponse(status=404)
        
        return response 


def state_create(request):

    response = None
    data = json.loads(request.body)

    try:
        
        with transaction.atomic():

            state = StateSerialiazer.deserealizer(data)
            state.save()
            
            response = HttpResponse(
                status=201,
                content=json.dumps([
                    StateSerialiazer.serealizer(state)
                ])
            )

    except Exception as e:
        
        response = HttpResponse(
            status=400,
            content=json.dumps({
                "Error": str(e)
            })
        )

    return response



def state_index(request):

    response = None

    if request.method == 'GET':

       response = state_list(request)
    
    if request.method == 'POST':
        
      response = state_create(request)
        
    return response