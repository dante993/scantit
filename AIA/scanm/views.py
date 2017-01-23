from django.shortcuts import render, redirect, get_object_or_404,render_to_response
from django.template import loader, context,RequestContext
from django.http import *

# Create your views here.
def v_inicio(request):
    mi_template = loader.get_template("index.html")
    return HttpResponse(mi_template.render())
