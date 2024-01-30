from django.http import HttpResponse

from .models import State

def state_index(request):

    query = State.objects.all()

    if query.exists():
        
        HttpResponse(status=200)
    else:

        return HttpResponse(status=404)

    

    return None

def by_id(request):
    
    return render(request, '/home/dev/Documents/estagio-mpto/tracker/index.html')