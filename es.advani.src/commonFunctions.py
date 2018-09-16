# -*- coding: utf-8 -*-

import urllib2
import numpy as np
import cv2

def translateWords(sentence):
    result=''
    flag = 0
    words=sentence.split(' ')
    for word in words:
        if flag==0:
            result=result+translateSingleWord(word)
            flag=1
        else: 
            result=result+'+'+translateSingleWord(word)
    return result

def translateSingleWord(word):
    finalWord=''
    result=word.decode('latin1')
    result= urllib2.quote(result.encode('utf-8'))
    separate=result.split('%83%C2')
    finalWord= ''.join(separate)
    return finalWord

def unicode_input(prompt):
    return raw_input(prompt).decode('latin1')

#funcion para extraer imagen a partir de url, fuente: 
#https://www.pyimagesearch.com/2015/03/02/convert-url-to-image-with-python-and-opencv/

def url_to_image(url):

	resp = urllib2.urlopen(url)
	image = np.asarray(bytearray(resp.read()), dtype="uint8")
	image = cv2.imdecode(image, cv2.IMREAD_COLOR)
	return image


def getSearchInput():
    result=''
    flag=0
    elemento = unicode_input("Introduzca la/s palabra/s a buscar, '%' como siguiente palabra para finalizar:\n")

    while elemento != '%':
        if flag == 0:
            result=urllib2.quote(elemento.encode('utf-8'))
        else:
            result=result+'+'+urllib2.quote(elemento.encode('utf-8'))
            
        elemento =unicode_input("siguiente palabra:\n")
        flag=1

    return result