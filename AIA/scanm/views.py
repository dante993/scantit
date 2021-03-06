# -*- coding: utf-8 -*-
import numpy as np
import tensorflow as tf
import cv2
from math import pow,sqrt
from django.shortcuts import render, redirect, get_object_or_404,render_to_response
from django.template import loader, context,RequestContext
from django.http import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
import time
import ftplib
import os
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
import sys
from scanm.forms import *
from os import listdir
from os.path import isfile, join
from PIL import Image, ImageFilter
import shutil
import subprocess

# variables con las credenciales para la conexion con el servidor ftp
ftp_servidor = '127.0.0.1'
ftp_usuario = 'scanm'
ftp_clave = 'scanm'

# Create your views here.
@login_required(login_url='/')
def v_inicio(request):
    usuario=get_object_or_404(Usuario,cedula=request.user)
    inicio_activacion='active'
    img_c_rec=Imagen.objects.count()
    admins_c=Usuario.object.filter(is_superuser=True).count()
    users_c=Usuario.object.filter(is_superuser=False).count()
    hc_c=Historial_clinico.objects.count()
    return render(request, "inicio.html",
                  {"hc_c":hc_c,"users_c":users_c,"admins_c":admins_c,"img_c_rec":img_c_rec,"usuario": usuario,"inicio_activacion":inicio_activacion})

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
def UsuarioUpdate(request,template_name='editar/profile_edit.html'):
    usuario=get_object_or_404(Usuario,cedula=request.user)
    form = Usuario_edtForm(request.POST or None, instance=usuario)
    fecha_n=str(usuario.fecha_de_nacimiento)
    if form.is_valid():
        usuario.nombres=request.POST.get("nombres")
        usuario.apellidos=request.POST.get("apellidos")
        usuario.e_mail=request.POST.get("e_mail")
        usuario.telefono=request.POST.get("telefono")
        usuario.direccion=request.POST.get("direccion")
        usuario.sexo=request.POST.get("sexo")
        usuario.fecha_de_nacimiento=request.POST.get("fecha_de_nacimiento")
        usuario.save()
        return redirect("inicio")
    return render(request,template_name,{'fecha_n':fecha_n,'form':form,'user':usuario})

@login_required(login_url='/')
def edt_password(request):
    usuario=get_object_or_404(Usuario,cedula=request.user)
    if request.method == 'POST':
        form = EditarContrasenaForm(request.POST)
        if form.is_valid():
            request.user.password = make_password(form.cleaned_data['password'])
            request.user.save()
            return redirect('logout')
    else:
        form = EditarContrasenaForm()
    return render(request, 'editar/password_edit.html', {'form': form,'user':usuario})

# ---------------------------------------------------------------------

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
                return redirect(request.POST.get('next', '/home/'))
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
        hist_c = Historial_clinico.objects.order_by("hc_apellido").filter(hc_id__contains=request.POST["busca"],hc_estado='Active',cedula=usuario)
        return render_to_response('listar/historial_clinico_list.html',{'historial':hist_c,'user':usuario})
    hist_c = Historial_clinico.objects.order_by("hc_apellido").filter(hc_estado='Active',cedula=usuario)
    return render_to_response('listar/historial_clinico_list.html',{'historial':hist_c,'user':usuario,'hc_activacion':hc_activacion})

@login_required(login_url='/')
def Historial_clinicoListin(request):
    usuario=get_object_or_404(Usuario,cedula=request.user)
    hc_activacion='active'
    if request.method=='POST':
        hist_c = Historial_clinico.objects.order_by("hc_apellido").filter(hc_id__contains=request.POST["busca"],hc_estado='Inactive',cedula=usuario)
        return render_to_response('listar/historial_clinico_list.html',{'historial':hist_c,'user':usuario})
    hist_c = Historial_clinico.objects.order_by("hc_apellido").filter(hc_estado='Inactive',cedula=usuario)
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
    hist_c = Historial_clinico.objects.order_by("hc_apellido").filter(hc_estado='Active',cedula=usuario)
    img_activacion='active'
    if form.is_valid():
        # id_im = Producto.objects.latest('img_id')+1
        id_im=int(Imagen.objects.all().count())+1
        ftp_raiz = 'user_detection' # Carpeta del servidor donde queremos subir el fichero
        fichero_destino = str(id_im)+'.jpg' # Nombre que tendra el fichero en el servidor
        data = request.FILES['img_ruta'] # or self.files['image'] in your form
        path = default_storage.save('tmp/'+str(usuario.cedula)+'/'+str(id_im)+'.jpg', ContentFile(data.read()))
        tmp_file = os.path.join(settings.MEDIA_ROOT)+"\\tmp\\"+str(usuario.cedula)+'\\'+str(id_im)+".jpg"
        convertir_a_jpg(tmp_file)
        try:
            ftp = ftplib.FTP(ftp_servidor, ftp_usuario, ftp_clave)
            ftp.cwd(ftp_raiz)
            ftp.mkd(str(usuario.cedula))
            ftp.quit()
        except:
        	print ("---------error-------" + ftp_servidor+" - ")
        try:
            ftp = ftplib.FTP(ftp_servidor, ftp_usuario, ftp_clave)
            ftp.cwd(ftp_raiz)
            ftp.cwd(str(usuario.cedula))
            try:
                f = open(tmp_file, 'rb')
                ftp.storbinary('STOR ' + fichero_destino, f)
                f.close()
                ftp.quit()
            except:
                print ("No se ha podido encontrar el fichero "+tmp_file+" - ")
        except:
        	print ("No se ha podido conectar al servidor " + ftp_servidor+" - ")
        ruta='ftp://'+ftp_usuario+':'+ftp_clave+'@127.0.0.1/user_detection/'+str(usuario.cedula)+'/'+fichero_destino
        descripcion=request.POST["img_descripcion"]
        fecha=str(time.strftime("%d/%m/%y"))
        hcc=request.POST["hc_cedula"]
        hcc_obj=get_object_or_404(Historial_clinico,hc_cedula=hcc)
        obj = Imagen(img_ruta=ruta,img_descripcion=descripcion,img_estado='Not analyzed',img_validez='Undefined',img_fecha=fecha,hc_cedula=hcc_obj)
        obj.save()
        os.remove(tmp_file)
        return redirect("imagen")
    return render(request,template_name,{'user':usuario,'form':form,"img_activacion":img_activacion})

@login_required(login_url='/')
def ImagenEvaluate(request,pk,template_name='listar/resultado_evaluacion.html'):
    usuario=get_object_or_404(Usuario,cedula=request.user)
    imagen=get_object_or_404(Imagen,img_id=pk)
    img_activacion='active'
    try:
        os.mkdir(os.path.join(settings.MEDIA_ROOT)+"\\reco\\"+str(usuario.cedula)+"\\")
    except:
        pass
    tmp_file =''
    try:
        ftp = ftplib.FTP(ftp_servidor, ftp_usuario, ftp_clave)
        try:
            ftp.cwd('user_detection')
            ftp.cwd(str(usuario.cedula))
            ftp.retrbinary('RETR '+str(pk)+'.jpg', open(''+str(pk)+'.jpg', 'wb').write)
            tm_file=settings.BASE_DIR+"\\"+str(pk)+".jpg"
            shutil.move(tm_file, os.path.join(settings.MEDIA_ROOT)+"\\reco\\"+str(usuario.cedula)+"\\"+str(pk)+".jpg")
            tmp_file=os.path.join(settings.MEDIA_ROOT)+"\\reco\\"+str(usuario.cedula)+"\\"+str(pk)+".jpg"
            ftp.quit()
        except:
            print ("No se ha podido encontrar el fichero  - ")
    except :
        print ("No se ha podido conectar al servidor  - ")
    vre=tf.gfile.FastGFile(os.path.join(settings.BASE_DIR, 'static')+"\\cnn\\"+"retrained_graph.pb", 'rb')
    aplicar_filtro(tmp_file)
    etiqueta,porcentaje=reconocimiento(tmp_file,vre)
    obj=etiqueta,porcentaje
    os.remove(tmp_file)
    return render(request,template_name,{'imagen':imagen,'obj':obj,'etiqueta':etiqueta,'porcentaje':porcentaje,'user':usuario,'img_activacion':img_activacion})


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

# ------------------------------------------Imagen de aprendizaje-----------------------------------------
@login_required(login_url='/')
def Imagen_admEvaluate(request):
    usuario=get_object_or_404(Usuario,cedula=request.user)
    ad_img_activacion='active'
    tipos = Tipo_cancer.objects.order_by("tc_id").filter(tc_estado='activo')
    tips=[]
    for t in tipos:
        tips.append(str(t.tc_nombre))
    Evaluar_aprendizaje(tips)
    return redirect("adm_imagen")

@login_required(login_url='/')
def Imagen_admRetrain(request):
    usuario=get_object_or_404(Usuario,cedula=request.user)
    ad_img_activacion='active'
    pth=os.path.join(settings.BASE_DIR, 'static')
    pth2=os.path.join(settings.BASE_DIR, 'scanm')
    print("paso ... "+str(pth2))
    result=subprocess.call("python "+str(pth2)+"\\retrain.py --bottleneck_dir="+
    pth+"/cnn/bottlenecks --how_many_training_steps 500 --model_dir="+
    pth+"/cnn/inception --output_graph="+pth+"/cnn/retrained_graph.pb --output_labels="+
    pth+"/cnn/retrained_labels.txt --image_dir "+pth+"/cnn/imagenes "+
    "--print_misclassified_test_images "+
    "--testing_percentage=10 --validation_percentage=10")
    return redirect("adm_imagen")

class Obj_list:
    # esta clase nos permite crear un listado de directorios con su respectivo contenido para el aprendizaje
    def __init__(self, nombre, cantidad):
        self.nm = nombre
        self.cn = cantidad

@login_required(login_url='/')
def Imagen_admList(request):
    usuario=get_object_or_404(Usuario,cedula=request.user)
    ad_img_activacion='active'
    dirs_to_learn=[]
    tipos = Tipo_cancer.objects.order_by("tc_id").filter(tc_estado='activo')
    for i in tipos:
        dirs_to_learn.append(Obj_list(i.tc_nombre,len(os.listdir(os.path.join(settings.BASE_DIR, 'static')+"\\cnn\\imagenes\\"+str(i.tc_nombre)+""))))
    return render_to_response('listar/adm_imagen_list.html',{'dirs_to_learn':dirs_to_learn,'user':usuario,'ad_img_activacion':ad_img_activacion})

@login_required(login_url='/')
def Imagen_admCreate(request,pk,pk2, template_name='agregar/adm_imagen_create.html'):
    usuario=get_object_or_404(Usuario,cedula=request.user)
    ad_img_activacion='active'
    if request.method=='POST':
        data = request.FILES['imgad_ruta']
        fls = request.FILES.getlist('imgad_ruta')
        cont=int(pk2)
        dir_l=str(pk)
        for dt in fls:
            path = os.path.join(settings.MEDIA_ROOT)+"\\"+default_storage.save('tmp\\'+str(usuario.cedula)+'\\'+str(cont)+'.gif', ContentFile(dt.read()))
            convertir_a_jpg(path)
            os.remove(path)
            path=os.path.join(settings.MEDIA_ROOT)+'\\tmp\\'+str(usuario.cedula)+'\\'+str(cont)+'.jpg'
            aplicar_filtro(path)
            shutil.move(path, os.path.join(settings.BASE_DIR, 'static')+"\\cnn\\imagenes\\"+str(dir_l)+"\\"+str(cont)+".jpg")
            cont=cont+1
        return redirect("adm_imagen")
    return render(request,template_name,{"user":usuario,"ad_img_activacion":ad_img_activacion})

# ------------------------------------------tipo de cancer-----------------------------------------
@login_required(login_url='/')
def Tipo_cancerList(request):
    usuario=get_object_or_404(Usuario,cedula=request.user)
    tipo_c_activacion='active'
    # obtener archivos y cantidad de achivos por carpeta
    tip = Tipo_cancer.objects.order_by("tc_id").filter(tc_estado='activo')

    if request.method=='POST':
        tip = Tipo_cancer.objects.order_by("tc_id").filter(tc_nombre__contains=request.POST["busca"],tc_estado='activo')
        return render_to_response('listar/tipo_cancer_list.html',{'img':img,'user':usuario})
    return render_to_response('listar/tipo_cancer_list.html',{'tip':tip,'user':usuario,'tipo_c_activacion':tipo_c_activacion})

@login_required(login_url='/')
def Tipo_cancerListin(request):
    usuario=get_object_or_404(Usuario,cedula=request.user)
    tipo_c_activacion='active'
    if request.method=='POST':
        tip = Tipo_cancer.objects.order_by("tc_id").filter(tc_nombre__contains=request.POST["busca"],tc_estado='inactivo')
        return render_to_response('listar/tipo_cancer_listin.html',{'img':img,'user':usuario})
    tip = Tipo_cancer.objects.order_by("tc_id").filter(tc_estado='inactivo')
    return render_to_response('listar/tipo_cancer_listin.html',{'tip':tip,'user':usuario,'tipo_c_activacion':tipo_c_activacion})

@login_required(login_url='/')
def Tipo_cancerCreate(request, template_name='agregar/tipo_cancern_create.html'):
    usuario=get_object_or_404(Usuario,cedula=request.user)
    form = Tipo_cancerForm(request.POST or None)
    tipo_c_activacion='active'
    if request.method=='POST':
        n_directorio = request.POST["tc_nombre"]
        print("-------------------"+n_directorio)
        if form.is_valid():
            try:
                print("------------------------------")
                print(os.path.join(settings.BASE_DIR, 'static')+"\\cnn\\imagenes\\"+str(n_directorio))
                os.mkdir(os.path.join(settings.BASE_DIR, 'static')+"\\cnn\\imagenes\\"+str(n_directorio))
            except:
                print("Error - puede que este directorio ya exista")
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

def convertBMP(ruta,id_r):
    mypath=ruta
    onlyfiles = [ f for f in listdir(mypath) if isfile(join(mypath,f)) ]
    images = np.empty(len(onlyfiles), dtype=object)
    for n in range(0, len(onlyfiles)):
        images[n] = Image.open( join(mypath,onlyfiles[n]))
    for i, face in enumerate(images):
        face.save(ruta+"\\" + id_r + ".bmp")

def reconocimiento(image_path,vre):
    # definimos dos listas para almacenar los resultados
    etiqueta=[]
    porcentaje=[]
    # Read in the image_data
    image_data = tf.gfile.FastGFile(image_path, 'rb').read()

    # Loads label file, strips off carriage return
    label_lines = [line.rstrip() for line
                       in tf.gfile.GFile(os.path.join(settings.BASE_DIR, 'static')+"\\cnn\\"+"retrained_labels.txt")]

    # Unpersists graph from file
    graph_def = tf.GraphDef()
    graph_def.ParseFromString(vre.read())
    _ = tf.import_graph_def(graph_def, name='')

    with tf.Session() as sess:
        # Feed the image_data as input to the graph and get first prediction
        softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')

        predictions = sess.run(softmax_tensor, \
                 {'DecodeJpeg/contents:0': image_data})

        # Sort to show labels of first prediction in order of confidence
        top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]

        for node_id in top_k:
            human_string = label_lines[node_id]
            score = predictions[0][node_id]
            etiqueta.append(human_string)
            porcentaje.append(round(score*100,2))
            print('%s (score = %.5f)' % (human_string, score))
    return etiqueta,porcentaje

def convertir_a_jpg(archivo):
    cadena=str(archivo).split(".")
    Image.open(archivo).convert('RGB').save(str(cadena[0])+'.jpg', quality=95)

def aplicar_filtro(archivo):
    im = Image.open(archivo)
    imagen = Image.new("RGB", im.size, (255, 255, 255))
    imagen.paste(im)
    desenfocada = imagen.filter(ImageFilter.BLUR)
    contorneada = imagen.filter(ImageFilter.CONTOUR)
    detallar = imagen.filter(ImageFilter.DETAIL)
    realzarbordes = imagen.filter(ImageFilter.EDGE_ENHANCE_MORE)
    relieve = imagen.filter(ImageFilter.EMBOSS)
    limites = imagen.filter(ImageFilter.FIND_EDGES)
    suavizar = imagen.filter(ImageFilter.SMOOTH_MORE)
    afinar = imagen.filter(ImageFilter.SHARPEN)
    width, height =realzarbordes.size
    for w in range(width):
        for h in range(height):
            r, g, b =realzarbordes.getpixel((w, h))
            gray = (r+g+b)/3
            realzarbordes.putpixel((w, h), (255-r, 255-g, 255-b))
    realzarbordes.save(archivo)

def entrenar():
    result=subprocess.call("python "+os.path.join(settings.BASE_DIR, 'scanm')+"\\retrain.py --bottleneck_dir="+pth+"/cnn/bottlenecks --how_many_training_steps 500 --model_dir="+pth+"/cnn/inception --output_graph="+pth+"/cnn/retrained_graph.pb --output_labels="+pth+"/cnn/retrained_labels.txt --image_dir="+pth+"/cnn/imagenes")

def Evaluar_aprendizaje(etiquetas):
    vre=tf.gfile.FastGFile(os.path.join(settings.BASE_DIR, 'static')+"\\cnn\\"+"retrained_graph.pb", 'rb')
    cabecera=""
    linea="imagen,"+str(",".join(etiquetas))+"\n"
    cabecera=linea.replace("\n","")
    cabecera=cabecera.replace("imagen,","")
    cabecera=cabecera.split(",")

    for (base, dirs, files) in os.walk(os.path.join(settings.BASE_DIR, 'static')+"/cnn/imagenes/"):
        for dr in os.listdir(base):
            if os.path.isdir(os.path.join(base,dr)):
                for f in os.listdir(str(base)+'/'+str(dr)):
                    if os.path.isfile(os.path.join(base,dr,f)):
                        et,pr=reconocimiento(os.path.join(base,dr,f),vre)
                        # inicializar linea de escritura
                        row=[]
                        for i in range(len(cabecera)):
                            row.append("")
                        # -----------------------------

                        for i in range(len(pr)):
                            for j in range(len(cabecera)):
                                if str(et[i]).lower()==str(cabecera[j]).lower():
                                    row[j]=str(pr[i])
                        linea+=str(os.path.join(dr,f))+","+str(",".join(row))+"\n"
    archivo=open (os.path.join(settings.BASE_DIR, 'static')+"\\cnn\\eval\\eval.csv","a")
    archivo.write(linea)
    archivo.close()




#
