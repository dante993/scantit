#!/usr/bin/python
# -*- coding: utf-8 -*-
import numpy as np
import cv2
from math import pow,sqrt

#Tamaño del kernel
ksize = 31

#Valores del recuadro 
xR=4
yR=4
altoR=20
anchoR=20
dimR= altoR*anchoR
#dimensiones de la imagen 
altoI=360
anchoI=220
dim =altoI*anchoI

#Contador etiquetar para imagenes salientes
c=1

#Rutas de lectura y escritura de imagenes
rutaIn=''
rutaOut='Z:/Google Drive/ltobar_est/Decimo/AIA/tratoDeImagenes'

tipo=-1 #tipo de cancer o normal 

etiquetas=np.empty((dimR,1))
vecC=np.zeros((dimR,70))
#tetha es la orientacion
#gamma es la escala
#5 orientaciones * 7 escalas
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
	#creartxt()
	#Array de vectores caracteristicos, inicializados en zero
	count=0
	for x in np.arange(0,altoI):
		for y in np.arange(0,anchoI):
			if(x>=xR and x<(xR+anchoR) and y>=yR and y<(yR+altoR)):	
				vecC[count,index]=res[x,y]		
				if (index == 0):
				#print (str(x)+" >= "+str(xR)+" --- "+str(x)+" <= "+str(xR+anchoR)+" and "+str(y)+" >= "+str(yR)+" --- "+str(y)+" <= "+str(yR+anchoR))
					#print (str(x)+'-'+str(y))
					if(tipo==0):#normal
						etiquetas[count,0]=0
					if(tipo==1):#cancer
						etiquetas[count,0]=1
					if(tipo==-1):#benigno
						etiquetas[count,0]=-1
				count=count+1	

def grabarTxt(vec,etiquetas):
    archi=open('VC.txt','a')
    archi.write(str(vec)+'\n')
    archi.close()
    archi=open('VCEtiqueta.txt','a')
    archi.write(str(etiquetas)+'\n')
    archi.close()
				
if __name__ == '__main__':
    import sys
    try:
        img_fn = sys.argv[1]
    except:
		img_fn = cv2.imread( 'Z:/Google Drive/ltobar_est/Decimo/AIA/tratoDeImagenes/Casos/case4548/caso4548_left_cc.BMP' )
		img_gris=cv2.cvtColor(img_fn, cv2.COLOR_BGR2GRAY)
		new_imgGris=preProccess(img_gris)
		if img_gris is None:
			print 'Failed to load image file:', img_fn
			sys.exit(1)

			
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
		#cv2.imshow('result', new_imgGris)
		#k = cv2.waitKey(0)
		cv2.imwrite(rutaOut+'/GaborWavelet/case4548/GaborWavelet-'+str(c)+'.bmp',res1)
		cv2.imwrite(rutaOut+'/Gaussian/case4548/Gaussian-'+str(c)+'.bmp',res2)
		cv2.imwrite(rutaOut+'/DesviacionEstandar/case4548/DesviacionEstandar-'+str(c)+'.bmp',res3)
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
#for x in np.arange(0,dimR):
#	print (str(x))
#	print(etiquetas[x])