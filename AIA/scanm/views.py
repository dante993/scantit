# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect, get_object_or_404,render_to_response
from django.template import loader, context,RequestContext
from django.http import *
from forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import time
import ftplib
import os
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
import numpy as np
import cv2
from math import pow,sqrt
import sys
ftp_servidor = '127.0.0.1'
ftp_usuario = 'scanm'
ftp_clave = 'scanm'

# Create your views here.
@login_required(login_url='/')
def v_inicio(request):
    usuario=get_object_or_404(Usuario,cedula=request.user)
    inicio_activacion='active'
    img_c_apr=Imagen_adm.objects.count()
    img_c_rec=Imagen.objects.count()
    admins_c=Usuario.object.filter(is_superuser=True).count()
    users_c=Usuario.object.filter(is_superuser=False).count()
    hc_c=Historial_clinico.objects.count()
    return render(request, "inicio.html",
                  {"hc_c":hc_c,"users_c":users_c,"admins_c":admins_c,"img_c_rec":img_c_rec,"img_c_apr":img_c_apr,"usuario": usuario,"inicio_activacion":inicio_activacion})

def UsuaioC(request, template_name='agregar/usuario_create.html'):
    form = UsuarioForm(request.POST or None)
    if form.is_valid():
        cedula=request.POST.get("cedula")
        nombre=request.POST.get("nombres")
        apellido=request.POST.get("apellidos")
        e_mail=request.POST.get("e_mail")
        telefono=request.POST.get("telefono")
        direccion=request.POST.get("direccion")
        sexo=request.POST.get("sexo")
        fecha_de_nacimiento=request.POST.get("fecha_de_nacimiento")
        contra=request.POST.get("contra")

        Usuario.object.create_user(cedula,nombre,apellido,e_mail,contra,telefono=telefono,direccion=direccion,sexo=sexo,fecha_de_nacimiento=fecha_de_nacimiento)
        return redirect("login")

    return render(request,template_name,{'form':form})

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
        return render_to_response('listar/historial_clinico_list.html',{'historial':hist_c,'user':usuario})
    hist_c = Historial_clinico.objects.order_by("hc_apellido")
    return render_to_response('listar/historial_clinico_list.html',{'historial':hist_c,'user':usuario,'hc_activacion':hc_activacion})

@login_required(login_url='/')
def Historial_clinicoListin(request):
    usuario=get_object_or_404(Usuario,cedula=request.user)
    hc_activacion='active'
    if request.method=='POST':
        hist_c = Historial_clinico.objects.order_by("hc_apellido").filter(hc_id__contains=request.POST["busca"],hc_estado='inactivo')
        return render_to_response('listar/historial_clinico_list.html',{'historial':hist_c,'user':usuario})
    hist_c = Historial_clinico.objects.order_by("hc_apellido").filter(hc_estado='inactivo')
    return render_to_response('listar/historial_clinico_listin.html',{'historial':hist_c,'user':usuario,'hc_activacion':hc_activacion})

@login_required(login_url='/')
def Historial_clinicoCreate(request, template_name='agregar/Historial_clinico_create.html'):
    usuario=get_object_or_404(Usuario,cedula=request.user)
    form = Historial_clinicoForm(request.POST or None)
    hc_activacion='active'
    if form.is_valid():
        form.save()
        return redirect("historial_clinico")
    return render(request,template_name,{'form':form,'user':usuario,'hc_activacion':hc_activacion})

@login_required(login_url='/')
def Historial_clinicoUpdate(request,pk,template_name='agregar/Historial_clinico_create.html'):
    usuario=get_object_or_404(Usuario,cedula=request.user)
    obj = get_object_or_404(Historial_clinico, pk=pk)
    form = Historial_clinicoForm(request.POST or None, instance=obj)
    hc_activacion='active'
    if form.is_valid():
        form.save()
        return redirect("historial_clinico")
    return render(request,template_name,{'form':form,'user':usuario,'hc_activacion':hc_activacion})

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
        return render_to_response('listar/imagen_list.html',{'img':img,'user':usuario})
    img = Imagen.objects.order_by("img_fecha")
    return render_to_response('listar/imagen_list.html',{'img':img,'user':usuario,'img_activacion':img_activacion})

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
    return render(request,template_name,{'user':usuario,'form':form,"img_activacion":img_activacion})

@login_required(login_url='/')
def ImagenUpdate(request,pk,template_name='editar/imagen_update.html'):
    usuario=get_object_or_404(Usuario,cedula=request.user)
    obj = get_object_or_404(Imagen, pk=pk)
    form = ImagenForm(request.POST or None, instance=obj)
    img_activacion='active'
    if form.is_valid():
        form.save()
        return redirect("imagen")
    return render(request,template_name,{'form':form,'user':usuario,'img_activacion':img_activacion})

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
        contador=int(request.POST["contar"])
        for i in range(contador-1):
            x=int(request.POST.get("x"+str(i+1)))
            y=int(request.POST.get("y"+str(i+1)))
            ancho=int(request.POST.get("ancho"+str(i+1)))
            alto=int(request.POST.get("alto"+str(i+1)))
            arobj = Area_imagen(arim_pos_x=x,arim_pos_y=y,arim_ancho=ancho,arim_alto=alto,imgad_id=img)
            arobj.save()
        # vc_aprendizaje(str(img.imgad_id))
        return redirect("adm_imagen")
    return render(request,template_name,{'user':usuario,'img':img,"ad_img_activacion":ad_img_activacion})

# ------------------------------------------Imagen de aprendizaje-----------------------------------------
@login_required(login_url='/')
def Imagen_admList(request):
    usuario=get_object_or_404(Usuario,cedula=request.user)
    ad_img_activacion='active'
    img = Imagen_adm.objects.order_by("imgad_fecha")
    return render_to_response('listar/adm_imagen_list.html',{'img':img,'user':usuario,'ad_img_activacion':ad_img_activacion})

@login_required(login_url='/')
def Imagen_admCreate(request, template_name='agregar/adm_imagen_create.html'):
    usuario=get_object_or_404(Usuario,cedula=request.user)
    form = Imagen_admForm(request.POST or None,request.FILES or None)
    ad_img_activacion='active'
    if form.is_valid():
        id_im=int(Imagen_adm.objects.all().count())
        id_im=id_im+1
        ftp_raiz = 'admin_learning' # Carpeta del servidor donde queremos subir el fichero
        fichero_destino = str(id_im)+'.gif' # Nombre que tendra el fichero en el servidor
        data = request.FILES['imgad_ruta'] # or self.files['image'] in your form
        path = default_storage.save('tmp/tmp.gif', ContentFile(data.read()))
        tmp_file = os.path.join(settings.MEDIA_ROOT)+"\\tmp\\tmp.gif"
        try:
            ftp = ftplib.FTP(ftp_servidor, ftp_usuario, ftp_clave)
            ftp.cwd(ftp_raiz)
            ftp.mkd(str(id_im))
            ftp.cwd(str(id_im))
            ftp.mkd("media")
            ftp.mkd("desviacion_estandar")
            ftp.mkd("gabor")
            try:
                f = open(tmp_file, 'rb')
                ftp.storbinary('STOR ' + fichero_destino, f)
                f.close()
                ftp.quit()
            except Exception,e2:
        		print "No se ha podido encontrar el fichero " + tmp_file+" - "+str(e2)
        except Exception,e:
        	print "No se ha podido conectar al servidor " + ftp_servidor+" - "+str(e)
        ruta='ftp://'+ftp_usuario+':'+ftp_clave+'@127.0.0.1/admin_learning/'+str(id_im)+'/'+fichero_destino
        descripcion=request.POST["imgad_descripcion"]
        fecha=str(time.strftime("%d/%m/%y"))
        ancho=request.POST["imgad_ancho"]
        alto=request.POST["imgad_alto"]
        tip=request.POST["tc_id"]
        tip_obj=get_object_or_404(Tipo_cancer, tc_id=tip)
        obj = Imagen_adm(imgad_ruta=ruta,imgad_descripcion=descripcion,imgad_fecha=fecha,imgad_ancho=ancho,imgad_alto=alto,imgad_estado='no aprendida',tc_id=tip_obj)
        obj.save()
        os.remove(tmp_file)
        return redirect("adm_imagen")
    return render(request,template_name,{'user':usuario,'form':form,"ad_img_activacion":ad_img_activacion})

@login_required(login_url='/')
def Imagen_admUpdate(request,pk,template_name='editar/imagen_update.html'):
    usuario=get_object_or_404(Usuario,cedula=request.user)
    obj = get_object_or_404(Imagen, pk=pk)
    form = Imagen_admForm(request.POST or None, instance=obj)
    ad_img_activacion='active'
    if form.is_valid():
        form.save()
        return redirect("imagen")
    return render(request,template_name,{'form':form,'user':usuario,'ad_img_activacion':ad_img_activacion})

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
        return render_to_response('listar/tipo_cancer_list.html',{'img':img,'user':usuario})
    tip = Tipo_cancer.objects.order_by("tc_nombre").filter(tc_estado='activo')
    return render_to_response('listar/tipo_cancer_list.html',{'tip':tip,'user':usuario,'tipo_c_activacion':tipo_c_activacion})

@login_required(login_url='/')
def Tipo_cancerListin(request):
    usuario=get_object_or_404(Usuario,cedula=request.user)
    tipo_c_activacion='active'
    if request.method=='POST':
        tip = Tipo_cancer.objects.order_by("tc_nombre").filter(tc_nombre__contains=request.POST["busca"],tc_estado='inactivo')
        return render_to_response('listar/tipo_cancer_listin.html',{'img':img,'user':usuario})
    tip = Tipo_cancer.objects.order_by("tc_nombre").filter(tc_estado='inactivo')
    return render_to_response('listar/tipo_cancer_listin.html',{'tip':tip,'user':usuario,'tipo_c_activacion':tipo_c_activacion})

@login_required(login_url='/')
def Tipo_cancerCreate(request, template_name='agregar/tipo_cancern_create.html'):
    usuario=get_object_or_404(Usuario,cedula=request.user)
    form = Tipo_cancerForm(request.POST or None)
    tipo_c_activacion='active'
    if form.is_valid():
        form.save()
        return redirect("tipo_cancer")
    return render(request,template_name,{'user':usuario,'form':form,"tipo_c_activacion":tipo_c_activacion})

@login_required(login_url='/')
def Tipo_cancerUpdate(request,pk,template_name='agregar/tipo_cancern_create.html'):
    usuario=get_object_or_404(Usuario,cedula=request.user)
    obj = get_object_or_404(Tipo_cancer, pk=pk)
    form = Tipo_cancerForm(request.POST or None, instance=obj)
    tipo_c_activacion='active'
    if form.is_valid():
        form.save()
        return redirect("tipo_cancer")
    return render(request,template_name,{'form':form,'user':usuario,'tipo_c_activacion':tipo_c_activacion})

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



# ...............................................................................................
from os import listdir
from os.path import isfile, join
import numpy
from PIL import Image
def vc_aprendizaje(id_r):
    import sys
    print("-----------------------------llego----------------------------")
    # ftp.retrbinary('RETR imagen.png', open('imagen2.png', 'wb').write)
    # path = default_storage.save('tmp/tmp.gif', ContentFile(data.read()))
    # tmp_file = os.path.join(settings.MEDIA_ROOT)+"\\tmp_dw\\tmp.gif"
    try:
        ftp = ftplib.FTP(ftp_servidor, ftp_usuario, ftp_clave)
        try:
            ftp.cwd('admin_learning')
            ftp.cwd(str(id_r))

            ftp.retrbinary('RETR '+id_r+'.gif', open(''+id_r+'.gif', 'wb').write)
            tmp_file=os.path.join(settings.BASE_DIR)+"\\"+id_r+".gif"
            path=os.path.join(settings.MEDIA_ROOT)+"\\tmp_dw\\"+id_r+".gif"
            os.rename(tmp_file, path)

            convertBMP(os.path.join(settings.MEDIA_ROOT)+"\\tmp_dw\\",id_r)
            os.remove(path)
            os.remove(tmp_file)
            ftp.quit()
        except Exception,e2:
            print "No se ha podido encontrar el fichero  - "+str(e2)
    except Exception,e:
        print "No se ha podido conectar al servidor  - "

    # try:
    #     img_fn = sys.argv[1]
    # except:
	# 	img_fn = cv2.imread(ruta_img)
	# 	img_gris=cv2.cvtColor(img_fn, cv2.COLOR_BGR2GRAY)
	# 	new_imgGris=preProccess(img_gris)
	# 	if img_gris is None:
	# 		print 'Failed to load image file:', img_fn
	# 		sys.exit(1)

def convertBMP(ruta,id_r):
    mypath=ruta
    onlyfiles = [ f for f in listdir(mypath) if isfile(join(mypath,f)) ]
    images = numpy.empty(len(onlyfiles), dtype=object)
    for n in range(0, len(onlyfiles)):
      images[n] = Image.open( join(mypath,onlyfiles[n]))

    for i, face in enumerate(images):
        face.save(ruta+"\\" + id_r + ".bmp")
