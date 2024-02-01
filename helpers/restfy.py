import json

from django.http import HttpResponse
from django.db import transaction



def make_rest(Serializer):

    Model = Serializer.Model()

    def _create(request):

        response = None
        data = json.loads(request.body)

        try:
            
            with transaction.atomic():

                instance = Serializer.deserealizer(data)
                instance.save()
                
                response = HttpResponse(
                    status=201,
                    content_type='application/json',
                    content=json.dumps(
                        Serializer.serealizer(instance)
                    )
                )

        except Exception as e:
            
            response = HttpResponse(
                status=400,
                content=json.dumps({
                    "Error": str(e)
                })
            )

        return response


    def _list(request):

        query = Model.objects.all()

        if query.exists():
            
            response = HttpResponse(
                content_type='application/json',
                content=json.dumps([
                    Serializer.serealizer(instance) for instance in query
                ])
                    
            )

            return response
        else:
            
            response = HttpResponse(status=404)
            
            return response 


    def _list_one(request, id):

        status=200
        result = {}

        try:
    
            result = [Serializer.serealizer(Model.objects.get(id=id))]

        except Model.DoesNotExist:

            status = 404
            result = {
                'Menssage': f'O id {id} não existe'
            }

        return HttpResponse(
            status=status,
            content_type='application/json',
            content=json.dumps(result)
        )


    def _delete(request, id):

        status=200
        result = {}

        try:
            instance = Model.objects.get(id=id)

            instance.delete()

            result = {
                'Mensage': 'Excluido com sucesso'
            }

            status=204

        except Model.DoesNotExist:
            
            status=404
            result = {
                'Menssage': f'O id {id} não existe no banco'
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

    def _update(request, id):
        
        status=200
        result = {}

        data = json.loads(request.body)

        try:

            with transaction.atomic():
                instance = Model.objects.get(id=id)

                for key, value in data.items():
                    setattr(instance, key, value)

                instance.save()

                result = Serializer.serealizer(instance)
            
        except Model.DoesNotExist:
            
            status=404
            result = {
                'Menssage': f'O id {id} não existe'
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


    def _index(request):

        response = None

        if request.method == 'GET':

           response =  _list(request)
    
        if request.method == 'POST':

            response =  _create(request)
        
        return response

    def _by_id(request, id):

        if request.method == 'GET':

            response = _list_one(request, id)
    
        elif request.method == 'DELETE':

            response = _delete(request, id)

        elif request.method == 'PUT':

            response = response = _update(request, id)

        return response

    return _index, _by_id