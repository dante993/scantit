from django.shortcuts import render, redirect, get_object_or_404,render_to_response
from django.template import loader, context,RequestContext
from django.http import *
from forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import time

# Create your views here.
# @login_required()
def v_inicio(request):
    usuario=get_object_or_404(Usuario,cedula=request.user)
    return render(request, "inicio.html", {"usuario": usuario})

@login_required()
def v_area_img(request):
    cargar_img_activacion='active'
    mi_template = loader.get_template("agregar/marcar_img.html")
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
                return redirect(request.POST.get('next', '/inicio/'))
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
    crear_hc_activacion='active'
    if form.is_valid():
        form.save()
        return redirect("area_img")
    return render(request,template_name,{'form':form,'usuario':usuario,'crear_hc_activacion':crear_hc_activacion})

# ------------------------------------------Imagen-----------------------------------------
@login_required(login_url='/')
def ImagenCreate(request, template_name='agregar/ImagenADD.html'):
    form = ImagenForm(request.POST or None,request.FILES or None)
    cargar_img_activacion='active'
    if form.is_valid():
        form.save()
        return redirect("inicio")
    # if request.method == 'POST':
    #     ruta=request.POST["img_ruta"]
    #     print(ruta)
    #     descripcion=request.POST["img_descripcion"]
    #     estado='no analizada'
    #     validez='no definido'
    #     fecha=str(time.strftime("%d/%m/%y"))
    #     hc=request.POST["hc_id"]
    #     hc_obj=get_object_or_404(Historial_clinico, hc_id=hc)
    #     obj = Imagen(img_ruta=ruta,img_descripcion=descripcion,img_estado=estado,img_validez=validez,img_fecha=fecha,hc_id=hc_obj)
    #     obj.save()
    #     return redirect("inicio")
    return render(request,template_name,{'form':form,"cargar_img_activacion":cargar_img_activacion})



# .............
