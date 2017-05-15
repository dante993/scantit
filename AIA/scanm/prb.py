import os
import subprocess
import time
import shutil

# shutil.rmtree(os.path.dirname(os.path.abspath(__file__))+"\\holaaa\\", ignore_errors=False, onerror=None)
# a="1,2,3"
# a=a.split(",")
# b=["5","2","4"]
# if b[1]==a[1]:
#     print(len(a))
          # Espera 1 segundo antes de continuar.
# archivo=open (os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+"/static/cnn/eval/eval.csv","a")
# archivo.write(s)
# archivo.close()
# print(s)
#
# for (base, dirs, files) in os.walk(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+"/static/cnn/imagenes/"):
#     for dr in os.listdir(base):
#         if os.path.isdir(os.path.join(base,dr)):
#             cont=0
#             for f in os.listdir(str(base)+'/'+str(dr)):
#                 if os.path.isfile(os.path.join(base,dr,f)):
#                     cont=cont+1
#                     print(os.path.join(base,dr,f))



# result=subprocess.call("python retrain.py --bottleneck_dir=./../static/cnn/bottlenecks --how_many_training_steps 500 --model_dir=./../static/cnn/inception --output_graph=./../static/cnn/retrained_graph.pb --output_labels=./../static/cnn/retrained_labels.txt --image_dir ./../static/cnn/imagenes")


    # shutil.move(tm_file, os.path.join(settings.MEDIA_ROOT)+"\\reco\\"+str(usuario.cedula)+"\\"+str(pk)+".jpg")
    # tmp_file=os.path.join(settings.MEDIA_ROOT)+"\\reco\\"+str(usuario.cedula)+"\\"+str(pk)+".jpg"
    # if request.method=='POST':id_imgad_ruta
    # if form.is_valid():
    #     id_im=int(Imagen_adm.objects.all().count())
    #     id_im=id_im+1
    #     ftp_raiz = 'admin_learning' # Carpeta del servidor donde queremos subir el fichero
    #     fichero_destino1 = str(id_im)+'.gif' # Nombre que tendra el fichero en el servidor
    #     fichero_destino2 = str(id_im)+'.bmp' # Nombre que tendra el fichero en el servidor
    #     data = request.FILES['imgad_ruta'] # or self.files['image'] in your form
    #     path = default_storage.save('tmp/'+str(usuario.cedula)+'/tmp.gif', ContentFile(data.read()))
    #     tmp_file1 = os.path.join(settings.MEDIA_ROOT)+"\\tmp\\"+str(usuario.cedula)+"\\tmp.gif"
    #     convertBMP(os.path.join(settings.MEDIA_ROOT)+"\\tmp\\"+str(usuario.cedula),'tmp')
    #     tmp_file2 = os.path.join(settings.MEDIA_ROOT)+"\\tmp\\"+str(usuario.cedula)+"\\tmp.bmp"
    #
    #     #intentamos crear una carpeta con el id del usuario
    #     try:
    #         ftp = ftplib.FTP(ftp_servidor, ftp_usuario, ftp_clave)
    #         ftp.cwd(ftp_raiz)
    #         ftp.mkd(str(usuario.cedula))
    #         ftp.quit()
    #     except Exception:
    #     	print ("---------error-------" + ftp_servidor+" - ")
    #
    #     # guardamos los archivos en el ftp
    #     try:
    #         ftp = ftplib.FTP(ftp_servidor, ftp_usuario, ftp_clave)
    #         ftp.cwd(ftp_raiz)
    #         ftp.cwd(str(usuario.cedula))
    #         ftp.mkd(str(id_im))
    #         ftp.cwd(str(id_im))
    #         try:
    #             f1 = open(tmp_file1, 'rb')
    #             f2 = open(tmp_file2, 'rb')
    #             ftp.storbinary('STOR ' + fichero_destino1, f1)
    #             ftp.storbinary('STOR ' + fichero_destino2, f2)
    #             f1.close()
    #             f2.close()
    #             ftp.quit()
    #         except e2:
    #             print ("No se ha podido encontrar el fichero " + tmp_file1+" - "+tmp_file2+" - "+str(e2))
    #     except e:
    #     	print ("No se ha podido conectar al servidor " + ftp_servidor+" - "+str(e))
    #     ruta='ftp://'+ftp_usuario+':'+ftp_clave+'@127.0.0.1/admin_learning/'+str(usuario.cedula)+'/'+str(id_im)+'/'+fichero_destino1
    #     descripcion=request.POST["imgad_descripcion"]
    #     fecha=str(time.strftime("%d/%m/%y"))
    #     ancho=request.POST["imgad_ancho"]
    #     alto=request.POST["imgad_alto"]
    #     tip=request.POST["tc_id"]
    #     tip_obj=get_object_or_404(Tipo_cancer, tc_id=tip)
    #     obj = Imagen_adm(imgad_ruta=ruta,imgad_descripcion=descripcion,imgad_fecha=fecha,imgad_ancho=ancho,imgad_alto=alto,imgad_estado='no aprendida',tc_id=tip_obj)
    #     obj.save()
    #     os.remove(tmp_file1)
    #     os.remove(tmp_file2)
    #     return redirect("adm_imagen")
