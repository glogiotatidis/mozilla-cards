# Create your views here.
from django.shortcuts import render_to_response
from django.core.context_processors import csrf

def index(request):
    if request.method == 'GET':
        c = {}
        c.update(csrf(request))
        return render_to_response("index.html", c)

    else:
        return render_to_response("index.html")
