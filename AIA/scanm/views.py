from django.shortcuts import render, redirect, get_object_or_404,render_to_response
from django.template import loader, context,RequestContext
from django.http import *
from forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import time
import ftplib
import os

# Create your views here.
@login_required(login_url='/')
def v_inicio(request):
    usuario=get_object_or_404(Usuario,cedula=request.user)
    return render(request, "inicio.html", {"usuario": usuario})

@login_required(login_url='/')
def v_area_img(request):
    cargar_img_activacion='active'
    mi_template = loader.get_template("agregar/marcar_img.html")
    return HttpResponse(mi_template.render())

def logoutView(request):
    logout(request)
    return redirect("/")

def loginView(request):
    mensaje="nada"
    form = LoginForm()
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['cedula'],
                                password=form.cleaned_data['password'])
            if user is not None and user.is_active:
                login(request, user)
                return redirect(request.POST.get('next', '/inicio/'))
            else:
                mensaje="Nombre de Usuario o clave Incorrecto"
                return render(request, "login.html", {"form": form,"mensaje":mensaje})
    return render(request, "login.html", {"form": form,"mensaje":mensaje})

# ------------------------------------------historial clinico-----------------------------------------
@login_required(login_url='/')
def Historial_clinicoList(request):
    usuario=get_object_or_404(Usuario,cedula=request.user)
    hc_activacion='active'
    if request.method=='POST':
        hist_c = Historial_clinico.objects.order_by("hc_apellido").filter(hc_id__contains=request.POST["busca"])
        return render_to_response('listar/historial_clinico_list.html',{'historial':hist_c,'usuario':usuario})
    hist_c = Historial_clinico.objects.order_by("hc_apellido")
    return render_to_response('listar/historial_clinico_list.html',{'historial':hist_c,'usuario':usuario,'hc_activacion':hc_activacion})

@login_required(login_url='/')
def Historial_clinicoListin(request):
    usuario=get_object_or_404(Usuario,cedula=request.user)
    hc_activacion='active'
    if request.method=='POST':
        hist_c = Historial_clinico.objects.order_by("hc_apellido").filter(hc_id__contains=request.POST["busca"],hc_estado='inactivo')
        return render_to_response('listar/historial_clinico_list.html',{'historial':hist_c,'usuario':usuario})
    hist_c = Historial_clinico.objects.order_by("hc_apellido").filter(hc_estado='inactivo')
    return render_to_response('listar/historial_clinico_listin.html',{'historial':hist_c,'usuario':usuario,'hc_activacion':hc_activacion})

@login_required(login_url='/')
def Historial_clinicoCreate(request, template_name='agregar/Historial_clinico_create.html'):
    usuario=get_object_or_404(Usuario,cedula=request.user)
    form = Historial_clinicoForm(request.POST or None)
    hc_activacion='active'
    if form.is_valid():
        form.save()
        return redirect("historial_clinico")
    return render(request,template_name,{'form':form,'usuario':usuario,'hc_activacion':hc_activacion})

@login_required(login_url='/')
def Historial_clinicoUpdate(request,pk,template_name='agregar/Historial_clinico_create.html'):
    usuario=get_object_or_404(Usuario,cedula=request.user)
    obj = get_object_or_404(Historial_clinico, pk=pk)
    form = Historial_clinicoForm(request.POST or None, instance=obj)
    hc_activacion='active'
    if form.is_valid():
        form.save()
        return redirect("historial_clinico")
    return render(request,template_name,{'form':form,'usuario':usuario,'hc_activacion':hc_activacion})

@login_required(login_url='/')
def Historial_clinicoDelete(request,pk):
    obj = get_object_or_404(Historial_clinico, pk=pk)
    obj.hc_estado='inactivo'
    obj.save()
    return redirect("historial_clinico")
@login_required(login_url='/')
def Historial_clinicoRestore(request,pk):
    obj = get_object_or_404(Historial_clinico, pk=pk)
    obj.hc_estado='activo'
    obj.save()
    return redirect("historial_clinico")

# ------------------------------------------Imagen-----------------------------------------
@login_required(login_url='/')
def ImagenList(request):
    usuario=get_object_or_404(Usuario,cedula=request.user)
    img_activacion='active'
    if request.method=='POST':
        img = Imagen.objects.order_by("img_fecha").filter(img_ruta__contains=request.POST["busca"])
        return render_to_response('listar/imagen_list.html',{'img':img,'usuario':usuario})
    img = Imagen.objects.order_by("img_fecha")
    return render_to_response('listar/imagen_list.html',{'img':img,'usuario':usuario,'img_activacion':img_activacion})

@login_required(login_url='/')
def ImagenCreate(request, template_name='agregar/imagen_create.html'):
    usuario=get_object_or_404(Usuario,cedula=request.user)
    form = ImagenForm(request.POST or None,request.FILES or None)
    img_activacion='active'
    if form.is_valid():
        form.save()
        return redirect("imagen")
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
    return render(request,template_name,{'usuario':usuario,'form':form,"img_activacion":img_activacion})

@login_required(login_url='/')
def ImagenUpdate(request,pk,template_name='editar/imagen_update.html'):
    usuario=get_object_or_404(Usuario,cedula=request.user)
    obj = get_object_or_404(Imagen, pk=pk)
    form = ImagenForm(request.POST or None, instance=obj)
    img_activacion='active'
    if form.is_valid():
        form.save()
        return redirect("imagen")
    return render(request,template_name,{'form':form,'usuario':usuario,'img_activacion':img_activacion})

@login_required(login_url='/')
def ImagenDelete(request,pk):
    obj = get_object_or_404(Imagen, pk=pk)
    obj.img_validez='no valida'
    obj.save()
    return redirect("imagen")

# ------------------------------------------Area_Imagen-----------------------------------------
@login_required(login_url='/')
def Area_imagenCreate(request,pk, template_name='agregar/area_imagen_create.html'):
    usuario=get_object_or_404(Usuario,cedula=request.user)
    img=get_object_or_404(Imagen_adm, pk=pk)
    ad_img_activacion='active'
    if request.method == 'POST':
        # ruta=request.POST["img_ruta"]
        # print(ruta)
        # descripcion=request.POST["img_descripcion"]
        # estado='no analizada'
        # validez='no definido'
        # fecha=str(time.strftime("%d/%m/%y"))
        # hc=request.POST["hc_id"]
        # hc_obj=get_object_or_404(Historial_clinico, hc_id=hc)
        # obj = Imagen(img_ruta=ruta,img_descripcion=descripcion,img_estado=estado,img_validez=validez,img_fecha=fecha,hc_id=hc_obj)
        # obj.save()
        return redirect("imagen")
    return render(request,template_name,{'usuario':usuario,'img':img,"ad_img_activacion":ad_img_activacion})

# ------------------------------------------Imagen de aprendizaje-----------------------------------------
@login_required(login_url='/')
def Imagen_admList(request):
    usuario=get_object_or_404(Usuario,cedula=request.user)
    ad_img_activacion='active'
    if request.method=='POST':
        img = Imagen_adm.objects.order_by("imgad_fecha").filter(imgad_ruta__contains=request.POST["busca"])
        return render_to_response('listar/adm_imagen_list.html',{'img':img,'usuario':usuario})
    img = Imagen_adm.objects.order_by("imgad_fecha")
    return render_to_response('listar/adm_imagen_list.html',{'img':img,'usuario':usuario,'ad_img_activacion':ad_img_activacion})

@login_required(login_url='/')
def Imagen_admCreate(request, template_name='agregar/adm_imagen_create.html'):
    usuario=get_object_or_404(Usuario,cedula=request.user)
    form = Imagen_admForm(request.POST or None,request.FILES or None)
    ad_img_activacion='active'
    if form.is_valid():
        # Datos FTP
        ftp_servidor = 'ftp://127.0.0.1/'
        ftp_usuario  = 'anonymous'
        ftp_clave    = ''
        ftp_raiz     = '/admin_learning' # Carpeta del servidor donde queremos subir el fichero

        # Datos del fichero a subir
        fichero_origen = request.FILES['imgad_ruta'] # Ruta al fichero que vamos a subir
        fichero_destino = 'image.gif' # Nombre que tendra el fichero en el servidor
        # Conectamos con el servidor
        try:
        	s = ftplib.FTP(ftp_servidor, ftp_usuario, ftp_clave)
        	try:
        		f = open(fichero_origen, 'rb')
        		s.cwd(ftp_raiz)
        		s.storbinary('STOR ' + fichero_destino, f)
        		f.close()
        		s.quit()
        	except Exception,e2:
        		print "No se ha podido encontrar el fichero " + fichero_origen+" - "+str(e2)
        except Exception,e:
        	print "No se ha podido conectar al servidor " + ftp_servidor+" - "+str(e)
        form.save()
        return redirect("adm_imagen")
    return render(request,template_name,{'usuario':usuario,'form':form,"ad_img_activacion":ad_img_activacion})

@login_required(login_url='/')
def Imagen_admUpdate(request,pk,template_name='editar/imagen_update.html'):
    usuario=get_object_or_404(Usuario,cedula=request.user)
    obj = get_object_or_404(Imagen, pk=pk)
    form = Imagen_admForm(request.POST or None, instance=obj)
    ad_img_activacion='active'
    if form.is_valid():
        form.save()
        return redirect("imagen")
    return render(request,template_name,{'form':form,'usuario':usuario,'ad_img_activacion':ad_img_activacion})

@login_required(login_url='/')
def Imagen_admDelete(request,pk):
    obj = get_object_or_404(Imagen, pk=pk)
    obj.img_validez='no valida'
    obj.save()
    return redirect("imagen")

# ------------------------------------------tipo de cancer-----------------------------------------
@login_required(login_url='/')
def Tipo_cancerList(request):
    usuario=get_object_or_404(Usuario,cedula=request.user)
    tipo_c_activacion='active'
    if request.method=='POST':
        tip = Tipo_cancer.objects.order_by("tc_nombre").filter(tc_nombre__contains=request.POST["busca"],tc_estado='activo')
        return render_to_response('listar/tipo_cancer_list.html',{'img':img,'usuario':usuario})
    tip = Tipo_cancer.objects.order_by("tc_nombre").filter(tc_estado='activo')
    return render_to_response('listar/tipo_cancer_list.html',{'tip':tip,'usuario':usuario,'tipo_c_activacion':tipo_c_activacion})

@login_required(login_url='/')
def Tipo_cancerListin(request):
    usuario=get_object_or_404(Usuario,cedula=request.user)
    tipo_c_activacion='active'
    if request.method=='POST':
        tip = Tipo_cancer.objects.order_by("tc_nombre").filter(tc_nombre__contains=request.POST["busca"],tc_estado='inactivo')
        return render_to_response('listar/tipo_cancer_listin.html',{'img':img,'usuario':usuario})
    tip = Tipo_cancer.objects.order_by("tc_nombre").filter(tc_estado='inactivo')
    return render_to_response('listar/tipo_cancer_listin.html',{'tip':tip,'usuario':usuario,'tipo_c_activacion':tipo_c_activacion})

@login_required(login_url='/')
def Tipo_cancerCreate(request, template_name='agregar/tipo_cancern_create.html'):
    usuario=get_object_or_404(Usuario,cedula=request.user)
    form = Tipo_cancerForm(request.POST or None)
    tipo_c_activacion='active'
    if form.is_valid():
        form.save()
        return redirect("tipo_cancer")
    return render(request,template_name,{'usuario':usuario,'form':form,"tipo_c_activacion":tipo_c_activacion})

@login_required(login_url='/')
def Tipo_cancerUpdate(request,pk,template_name='agregar/tipo_cancern_create.html'):
    usuario=get_object_or_404(Usuario,cedula=request.user)
    obj = get_object_or_404(Tipo_cancer, pk=pk)
    form = Tipo_cancerForm(request.POST or None, instance=obj)
    tipo_c_activacion='active'
    if form.is_valid():
        form.save()
        return redirect("tipo_cancer")
    return render(request,template_name,{'form':form,'usuario':usuario,'tipo_c_activacion':tipo_c_activacion})

@login_required(login_url='/')
def Tipo_cancerDelete(request,pk):
    obj = get_object_or_404(Tipo_cancer, pk=pk)
    obj.tc_estado='inactivo'
    obj.save()
    return redirect("tipo_cancer")

@login_required(login_url='/')
def Tipo_cancerDeleteP(request,pk):
    obj = get_object_or_404(Tipo_cancer, pk=pk)
    obj.delete()
    return redirect("tipo_cancer_in")

@login_required(login_url='/')
def Tipo_cancerRestore(request,pk):
    obj = get_object_or_404(Tipo_cancer, pk=pk)
    obj.tc_estado='activo'
    obj.save()
    return redirect("tipo_cancer_in")



# .............
