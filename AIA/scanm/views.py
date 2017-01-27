from django.shortcuts import render, redirect, get_object_or_404,render_to_response
from django.template import loader, context,RequestContext
from django.http import *
from forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import time

# Create your views here.
# @login_required()
def v_cargar_img(request):
    mi_template = loader.get_template("cargar_img.html")
    return HttpResponse(mi_template.render())

def logoutView(request):
    logout(request)
    return redirect("/")

def loginView(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['cedula'],
                                password=form.cleaned_data['password'])
            if user is not None and user.is_active:
                login(request, user)
                return redirect(request.POST.get('next', '/area_imagen/'))
            else:
                messages.error(request, "Nombre de Usuario o clave Incorrecto")
                return redirect("/login/")
    form = LoginForm()
    return render(request, "login.html", {"form": form})

# ------------------------------------------historial clinico-----------------------------------------
@login_required(login_url='/')
def Historial_clinicoCreate(request, template_name='agregar/Historial_clinicoADD.html'):
    usuario=get_object_or_404(Usuario,cedula=request.user)
    form = Historial_clinicoForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("area_img")
    return render(request,template_name,{'form':form,'usuario':usuario})

# ------------------------------------------Imagen-----------------------------------------
@login_required(login_url='/')
def ImagenCreate(request, template_name='agregar/ImagenADD.html'):
    form = ImagenForm()
    if request.method == 'POST':
        print("1")
        form=ImagenForm(request.POST or None,request.FILES)
        print("3")
        if form.is_valid():
            print("3")
            form.save()
            return redirect("area_img")
    return render(request,template_name,{'form':form})



# .............
