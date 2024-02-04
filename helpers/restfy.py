import json

from django.http import HttpResponse, HttpResponseNotAllowed
from django.db import transaction
from django.db.models import Q



def make_rest(
    Serializer, allow_list=True,  allow_create=True, 
    allow_list_by_id=True, allow_delete=True, allow_update=True
):

    Model = Serializer.Model()
    
        
    def _do_filter(base_query, filter):

        data = json.loads(filter) if filter else []
        stages = {}

        for expression in data:

            stage_number = expression.get('stage', 1)
            stage = stages.get(stage_number, [])

            if stage_number >= 0:

                stage.append(
                    Q(**{
                        expression.get('property'): expression.get('value')
                    })
                )
            else:

                 stage.append(
                    ~Q(**{
                        expression.get('property'): expression.get('value')
                    })
                )
            stages.update({stage_number:stage}) 

        sub_query = None
        query = None
       
        for stage_number in stages.keys():
           
            expressions = stages.get(stage_number)

            for expression in expressions:
                if not sub_query:
                    sub_query = expression
                else:
                    sub_query |= expression
            if not query:
                query = sub_query
            else:
                query &= sub_query
        print(query)
        return base_query.filter(query) if query else base_query


    def _list(request):

        status=200
        result = []

        try:

            query = Model.objects.all()
           
            query = _do_filter(query, request.GET.get('filters'))
                
            if query.exists():
                
                result = [Serializer.encode(instance) for instance in query]
            else:

                status=404

        except Exception as e:
            
            status=400
            result = {
                "Err": str(e)
            }
           
        return HttpResponse(
            status=status,
            content_type='application/json',
            content=json.dumps(result)
        ) 
        

    def _create(request):

        response = None
        data = json.loads(request.body)

        try:
            
            with transaction.atomic():

                instance = Serializer.decode(data)
                
                instance.save()
                response = HttpResponse(
                    status=201,
                    content_type='application/json',
                    content=json.dumps(
                        Serializer.encode(instance)
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


    def _list_one(request, id):

        status=200
        result = {}

        try:
    
            result = [Serializer.encode(Model.objects.get(id=id))]

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

                result = Serializer.encode(instance)
            
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

        if allow_list and request.method == 'GET':

           response =  _list(request)
    
        elif allow_create and request.method == 'POST':

            response =  _create(request)
        
        else:
            permite_method = []
            allow_create and permite_method.append('CREATE')
            allow_list and permite_method.append('GET')
   
            response = HttpResponseNotAllowed(permite_method)
            
        return response


    def _by_id(request, id):

        if allow_list_by_id and request.method == 'GET':

            response = _list_one(request, id)
    
        elif allow_delete and request.method == 'DELETE':

            response = _delete(request, id)

        elif allow_update and request.method == 'PUT':

            response = response = _update(request, id)
        else:
            permite_method = []
            allow_list_by_id and permite_method.append('GET')
            allow_update and permite_method.append('PUT')
            allow_delete and permite_method.append('DELETE')
                
            response = HttpResponseNotAllowed(permite_method)

        return response

    return _index, _by_id