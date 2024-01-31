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

def state_list_by_id(request, id):

    status=200
    result = {}

    try:
 
        result = StateSerialiazer.serealizer(State.objects.get(id=id))

    except State.DoesNotExist:

        status = 404
        result = {
            'Menssage': f'Estado com a id {id} não existe'
        }


    return HttpResponse(
        status=status,
        content_type='application/json',
        content=json.dumps(result)
    )

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

def state_delete_by_id(request, id):
    
    status=200
    result = {}

    try:
        state = State.objects.get(id=id)

        state.delete()

        result = {
            'Mensage': 'Estado Excluido com sucessso'
        }

        status=204

    except State.DoesNotExist:
        
        status=404
        result = {
            'Menssage': f'O Estado com a id {id} não existe'
        }

    except Exception as e:

        status=400

        result = {
            'Mensage': str(e)
        }
    
    return HttpResponse(
        status=status,
        content_type='application/json',
        content=json.dumps(result)
    )


def state_by_id(request, id):

    if request.method == 'GET':

        response = state_list_by_id(request, id)
    
    elif request.method == 'DELETE':

        response = state_delete_by_id(request, id)

    elif request.method == 'PUT':
        pass 

    

    return response