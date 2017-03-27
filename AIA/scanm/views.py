# -*- coding: utf-8 -*-
import numpy as np
import cv2
from math import pow,sqrt
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
import sys
ftp_servidor = '127.0.0.1'
ftp_usuario = 'scanm'
ftp_clave = 'scanm'

# Create your views here.
@login_required(login_url='/')
def v_inicio(request):
    usuario=get_object_or_404(Usuario,cedula=request.user)
    inicio_activacion='active'
    img_c_apr=Imagen_adm.objects.filter(imgad_estado='aprendida').count()
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
        hist_c = Historial_clinico.objects.order_by("hc_apellido").filter(hc_id__contains=request.POST["busca"],hc_estado='activo')
        return render_to_response('listar/historial_clinico_list.html',{'historial':hist_c,'user':usuario})
    hist_c = Historial_clinico.objects.order_by("hc_apellido").filter(hc_estado='activo')
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
def Historial_clinicoDeleteP(request,pk):
    obj = get_object_or_404(Historial_clinico, pk=pk)
    obj.delete()
    return redirect("historial_clinicoin")

@login_required(login_url='/')
def Historial_clinicoRestore(request,pk):
    obj = get_object_or_404(Historial_clinico, pk=pk)
    obj.hc_estado='activo'
    obj.save()
    return redirect("historial_clinicoin")

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

        id_im=int(Imagen.objects.all().count())
        id_im=id_im+1
        ftp_raiz = 'user_detection' # Carpeta del servidor donde queremos subir el fichero
        fichero_destino = str(id_im)+'.gif' # Nombre que tendra el fichero en el servidor
        data = request.FILES['img_ruta'] # or self.files['image'] in your form
        path = default_storage.save('tmp/'+str(id_im)+'.gif', ContentFile(data.read()))
        tmp_file = os.path.join(settings.MEDIA_ROOT)+"\\tmp\\"+str(id_im)+".gif"
        try:
            ftp = ftplib.FTP(ftp_servidor, ftp_usuario, ftp_clave)
            ftp.cwd(ftp_raiz)
            ftp.mkd(str(usuario.cedula))
            ftp.quit()
        except Exception,e:
        	print "---------error-------" + ftp_servidor+" - "+str(e)
        try:
            ftp = ftplib.FTP(ftp_servidor, ftp_usuario, ftp_clave)
            ftp.cwd(ftp_raiz)
            ftp.cwd(str(usuario.cedula))
            try:
                f = open(tmp_file, 'rb')
                ftp.storbinary('STOR ' + fichero_destino, f)
                f.close()
                ftp.quit()
            except Exception,e2:
        		print "No se ha podido encontrar el fichero " + tmp_file+" - "+str(e2)
        except Exception,e:
        	print "No se ha podido conectar al servidor " + ftp_servidor+" - "+str(e)
        ruta='ftp://'+ftp_usuario+':'+ftp_clave+'@127.0.0.1/user_detection/'+str(usuario.cedula)+'/'+fichero_destino
        descripcion=request.POST["img_descripcion"]
        fecha=str(time.strftime("%d/%m/%y"))
        hcc=request.POST["hc_cedula"]
        hcc_obj=get_object_or_404(Historial_clinico,hc_cedula=hcc)
        obj = Imagen(img_ruta=ruta,img_descripcion=descripcion,img_estado='no analizada',img_validez='no definido',img_fecha=fecha,hc_cedula=hcc_obj)
        obj.save()
        os.remove(tmp_file)
        return redirect("imagen")
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
        for i in range(contador):
            x=int(request.POST.get("x"+str(i+1)))
            y=int(request.POST.get("y"+str(i+1)))
            ancho=int(request.POST.get("ancho"+str(i+1)))
            alto=int(request.POST.get("alto"+str(i+1)))
            arobj = Area_imagen(arim_pos_x=x,arim_pos_y=y,arim_ancho=ancho,arim_alto=alto,imgad_id=img)
            arobj.save()
        vc_aprendizaje(str(img.imgad_id),str(usuario.cedula),str(img.tc_id))
        img.imgad_estado='aprendida'
        img.save()
        return render_to_response(template_name,{'user':usuario,'img':img,"ad_img_activacion":ad_img_activacion})
    return render(request,template_name,{'user':usuario,'img':img,"ad_img_activacion":ad_img_activacion})

# ------------------------------------------Imagen de aprendizaje-----------------------------------------
@login_required(login_url='/')
def Imagen_admList(request):
    usuario=get_object_or_404(Usuario,cedula=request.user)
    ad_img_activacion='active'
    img = Imagen_adm.objects.order_by("imgad_fecha").filter(imgad_estado='no aprendida')
    return render_to_response('listar/adm_imagen_list.html',{'img':img,'user':usuario,'ad_img_activacion':ad_img_activacion})

@login_required(login_url='/')
def Imagen_admListap(request):
    usuario=get_object_or_404(Usuario,cedula=request.user)
    ad_img_activacion='active'
    img = Imagen_adm.objects.order_by("imgad_fecha").filter(imgad_estado='aprendida')
    return render_to_response('listar/adm_imagen_listap.html',{'img':img,'user':usuario,'ad_img_activacion':ad_img_activacion})

@login_required(login_url='/')
def Imagen_admCreate(request, template_name='agregar/adm_imagen_create.html'):
    usuario=get_object_or_404(Usuario,cedula=request.user)
    form = Imagen_admForm(request.POST or None,request.FILES or None)
    ad_img_activacion='active'
    if form.is_valid():
        id_im=int(Imagen_adm.objects.all().count())
        id_im=id_im+1
        ftp_raiz = 'admin_learning' # Carpeta del servidor donde queremos subir el fichero
        fichero_destino1 = str(id_im)+'.gif' # Nombre que tendra el fichero en el servidor
        fichero_destino2 = str(id_im)+'.bmp' # Nombre que tendra el fichero en el servidor
        data = request.FILES['imgad_ruta'] # or self.files['image'] in your form
        path = default_storage.save('tmp/'+str(usuario.cedula)+'/tmp.gif', ContentFile(data.read()))
        tmp_file1 = os.path.join(settings.MEDIA_ROOT)+"\\tmp\\"+str(usuario.cedula)+"\\tmp.gif"
        convertBMP(os.path.join(settings.MEDIA_ROOT)+"\\tmp\\"+str(usuario.cedula),'tmp')
        tmp_file2 = os.path.join(settings.MEDIA_ROOT)+"\\tmp\\"+str(usuario.cedula)+"\\tmp.bmp"

        #intentamos crear una carpeta con el id del usuario
        try:
            ftp = ftplib.FTP(ftp_servidor, ftp_usuario, ftp_clave)
            ftp.cwd(ftp_raiz)
            ftp.mkd(str(usuario.cedula))
            ftp.quit()
        except Exception,e:
        	print "---------error-------" + ftp_servidor+" - "+str(e)

        # guardamos los archivos en el ftp
        try:
            ftp = ftplib.FTP(ftp_servidor, ftp_usuario, ftp_clave)
            ftp.cwd(ftp_raiz)
            ftp.cwd(str(usuario.cedula))
            ftp.mkd(str(id_im))
            ftp.cwd(str(id_im))
            try:
                f1 = open(tmp_file1, 'rb')
                f2 = open(tmp_file2, 'rb')
                ftp.storbinary('STOR ' + fichero_destino1, f1)
                ftp.storbinary('STOR ' + fichero_destino2, f2)
                f1.close()
                f2.close()
                ftp.quit()
            except Exception,e2:
        		print "No se ha podido encontrar el fichero " + tmp_file1+" - "+tmp_file2+" - "+str(e2)
        except Exception,e:
        	print "No se ha podido conectar al servidor " + ftp_servidor+" - "+str(e)
        ruta='ftp://'+ftp_usuario+':'+ftp_clave+'@127.0.0.1/admin_learning/'+str(usuario.cedula)+'/'+str(id_im)+'/'+fichero_destino1
        descripcion=request.POST["imgad_descripcion"]
        fecha=str(time.strftime("%d/%m/%y"))
        ancho=request.POST["imgad_ancho"]
        alto=request.POST["imgad_alto"]
        tip=request.POST["tc_id"]
        tip_obj=get_object_or_404(Tipo_cancer, tc_id=tip)
        obj = Imagen_adm(imgad_ruta=ruta,imgad_descripcion=descripcion,imgad_fecha=fecha,imgad_ancho=ancho,imgad_alto=alto,imgad_estado='no aprendida',tc_id=tip_obj)
        obj.save()
        os.remove(tmp_file1)
        os.remove(tmp_file2)
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
from PIL import Image
import shutil
def vc_aprendizaje(id_img,cedula,tip_cancer):
    #-------------descargando archivos del ftp---------------
    try:
        os.mkdir(os.path.join(settings.MEDIA_ROOT)+"\\tmp_dw\\"+cedula+"\\")
    except Exception,e_f:
        print("Error - "+str(e_f))
    path_tmp = os.path.join(settings.MEDIA_ROOT)+"\\tmp_dw\\"+cedula+"\\"
    tmp_file =''
    try:
        ftp = ftplib.FTP(ftp_servidor, ftp_usuario, ftp_clave)
        try:
            ftp.cwd('admin_learning')
            ftp.cwd(cedula)
            ftp.cwd(str(id_img))
            ftp.retrbinary('RETR '+id_img+'.bmp', open(''+id_img+'.bmp', 'wb').write)
            tm_file=os.path.join(settings.BASE_DIR)+"\\"+id_img+".bmp"
            shutil.move(tm_file, os.path.join(settings.MEDIA_ROOT)+"\\tmp_dw\\"+cedula+"\\"+id_img+".bmp")
            tmp_file=os.path.join(settings.MEDIA_ROOT)+"\\tmp_dw\\"+cedula+"\\"+id_img+".bmp"
            ftp.quit()
        except Exception,e2:
            print "No se ha podido encontrar el fichero  - "+str(e2)
    except Exception,e:
        print "No se ha podido conectar al servidor  - "
    #Tamaño del kernel
    ksize = 31
    areas=Area_imagen.objects.filter(imgad_id=id_img)
    for row in areas:
        xR=int(row.arim_pos_x)
        yR=int(row.arim_pos_y)
        altoR=int(row.arim_ancho)
        anchoR=int(row.arim_alto)
        dimR= altoR*anchoR
    #metodo para extraer ancho y alto de la imagen original de la bdd
    img_ad=Imagen_adm.objects.filter(imgad_id=id_img)
    for row in img_ad:
        altoI=int(row.imgad_alto)
        anchoI=int(row.imgad_ancho)
        dim =altoI*anchoI
    #Contador etiquetar para imagenes salientes
    c=1
    tipo=0 #tipo de cancer o normal
    etiquetas=np.empty((dimR,1))
    vecC=np.zeros((dimR,70))
    def build_filters(theta, gamma):
        filters = []
        kern = cv2.getGaborKernel((ksize, ksize), 4.0, theta, 10.0, gamma, 0, ktype=cv2.CV_32F)
        kern /= 1.5*kern.sum()
        filters.append(kern)
        return filters

    def process(img, filters):
        accum = np.zeros_like(img)
        for kern in filters:
            fimg = cv2.filter2D(img, cv2.CV_8UC3, kern)
            np.maximum(accum, fimg, accum)
        return accum

    #Aplicacion del filtro Gaussiano para obtener la Media
    def GaussianFilter(img):
        blur = cv2.GaussianBlur(img,(ksize,ksize),0)
        return blur

    def Desviacion_estandar(gaborWavelet,gaussiano):
        res = gaborWavelet-gaussiano #convolucion entre resultantes de filtros
        pot = res*res
        res1=GaussianFilter(pot)
        raiz=np.sqrt(res1)
        return raiz

    def preProccess(img):
        new = np.zeros((altoI,anchoI))
        for x in np.arange(0,altoI):
            for y in np.arange(0,anchoI):
                new[x,y]=float(img[x,y])/255
        return new
    def llenarVC(res,index):
        count=0
        for x in np.arange(0,altoI):
            for y in np.arange(0,anchoI):
                if(x>=xR and x<(xR+anchoR) and y>=yR and y<(yR+altoR)):
                    vecC[count,index]=res[x,y]
                    if (index == 0):
                        if(tipo==0):#normal
                            etiquetas[count,0]=0
                        if(tipo==1):#cancer
                            etiquetas[count,0]=1
                        if(tipo==2):#benigno
                            etiquetas[count,0]=2
                    count=count+1

    def grabarTxt(vec,etiquetas):
        archi=open(''+path_tmp+'VC-'+id_img+'.txt','a')
        archi.write(str(vec)+'\n')
        archi.close()
        archi=open(''+path_tmp+'VCEtiqueta-'+id_img+'.txt','a')
        archi.write(str(etiquetas)+'\n')
        archi.close()

    try:
        img_fn = sys.argv[1]
        img_fn = cv2.imread( ''+tmp_file )
        img_gris=cv2.cvtColor(img_fn, cv2.COLOR_BGR2GRAY)
        new_imgGris=preProccess(img_gris)
        if img_gris is None:
            print 'Failed to load image file:', img_fn
            sys.exit(1)
    except Exception,err_in:
        print('Error - '+str(err_in))

    countIndex = 0
    for theta in np.arange(1,8):
        for gamma in np.arange(0.1,0.6, 0.1):
            filters = build_filters(theta, gamma) #Creamos el filtro gaborWavelet
            res1 = process(new_imgGris, filters)#Aplicando filtro GaborWavelet a imagenes originales
            res2=GaussianFilter(res1) #Aplicando Filtro Gaussiano a imagenes con filtro GaborWavelet
            res3=Desviacion_estandar(res1,res2)
            #print ("Res2 img "+str(countIndex))
            #print res2
            llenarVC(res2,countIndex)
            countIndex+=1
            #print ("Res3 img "+str(countIndex))
            #print res3
            llenarVC(res3,countIndex)
            countIndex+=1
            c+=1
            cv2.destroyAllWindows()

    for x in np.arange(0,dimR):
        strI=''
        for y in np.arange(0,70):
            if(y==69):
                strI=strI+str(vecC[x,y])+''
            else:
                strI=strI+str(vecC[x,y])+','
        grabarTxt(strI,int(etiquetas[x]))
    try:
        ftp = ftplib.FTP(ftp_servidor, ftp_usuario, ftp_clave)
        ftp.cwd('admin_learning')
        ftp.cwd(cedula)
        ftp.cwd(id_img)
        try:
            f1 = open(path_tmp+'VC-'+id_img+'.txt', 'rb')
            f2 = open(path_tmp+'VCEtiqueta-'+id_img+'.txt', 'rb')
            ftp.storbinary('STOR ' + 'VC-'+id_img+'.txt', f1)
            ftp.storbinary('STOR ' + 'VCEtiqueta-'+id_img+'.txt', f2)
            f1.close()
            f2.close()
            ftp.quit()
        except Exception,e2:
            print "No se ha podido encontrar el fichero " + tmp_file1+" - "+tmp_file2+" - "+str(e2)
    except Exception,e:
        print "No se ha podido conectar al servidor " + ftp_servidor+" - "+str(e)
    os.remove(tmp_file)
    os.remove(path_tmp+'VC-'+id_img+'.txt')
    os.remove(path_tmp+'VCEtiqueta-'+id_img+'.txt')

def convertBMP(ruta,id_r):
    mypath=ruta
    onlyfiles = [ f for f in listdir(mypath) if isfile(join(mypath,f)) ]
    images = np.empty(len(onlyfiles), dtype=object)
    for n in range(0, len(onlyfiles)):
        images[n] = Image.open( join(mypath,onlyfiles[n]))
    for i, face in enumerate(images):
        face.save(ruta+"\\" + id_r + ".bmp")
