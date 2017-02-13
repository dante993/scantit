"""
from os import listdir
from os.path import isfile, join
import numpy
import cv2

mypath='C:\Users\William Roa\Documents\ProyectosPython\CASO1'
onlyfiles = [ f for f in listdir(mypath) if isfile(join(mypath,f)) ]
images = numpy.empty(len(onlyfiles), dtype=object)
for n in range(0, len(onlyfiles)):
  images[n] = cv2.imread( join(mypath,onlyfiles[n]))

for i, face in enumerate(images):
    cv2.imwrite("foto-" + str(i) + ".bmp", face)

print "Convertido......."
"""
from os import listdir
from os.path import isfile, join
import numpy
from PIL import Image

mypath='C:\Users\William Roa\Documents\ProyectosPython\CASO1'
onlyfiles = [ f for f in listdir(mypath) if isfile(join(mypath,f)) ]
images = numpy.empty(len(onlyfiles), dtype=object)
for n in range(0, len(onlyfiles)):
  images[n] = Image.open( join(mypath,onlyfiles[n]))

for i, face in enumerate(images):
    face.save("foto-" + str(i) + ".bmp")
