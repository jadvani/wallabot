# -*- coding: utf-8 -*-
"""
Created on Fri Sep 14 09:57:33 2018

@author: Javier
"""

from requests import get
from bs4 import BeautifulSoup
import sys
import urllib2
import numpy as np
import cv2
import matplotlib.pyplot as plt #%matplotlib inline para que vaya saliendo

_stdin_encoding = sys.stdin.encoding or 'utf-8'

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
    total=''
    bandera=0
    elemento = unicode_input("Introduzca la/s palabra/s a buscar, '%' como siguiente palabra para finalizar:\n")

    while elemento != '%':
        if bandera == 0:
            total=urllib2.quote(elemento.encode('utf-8'))
        else:
            total=total+'+'+urllib2.quote(elemento.encode('utf-8'))
            
        elemento =unicode_input("siguiente palabra:\n")
        bandera=1

    return total




url = 'https://es.wallapop.com/search?kws='+getSearchInput()+'&catIds=&verticalId='
print('buscando...')
response = get(url)

html_soup = BeautifulSoup(response.text, 'html.parser')
type(html_soup)

product_titles = html_soup.find_all('a', class_ = 'product-info-title')
product_prices = html_soup.find_all('span', class_ = 'product-info-price')
product_descriptions = html_soup.find_all('p', class_ = 'product-info-description')
product_images = html_soup.find_all('img', class_ = 'card-product-image')
quantity = len(product_descriptions)
print('he encontrado '+str(quantity)+' resultados')

if quantity>=0:
    for x in range(0, quantity):
        img=url_to_image(product_images[x]['src'])
        plt.imshow(img)
        plt.show()
        print product_titles[x].get_text()+'->'+product_prices[x].get_text()+'\n'
        print product_descriptions[x].get_text()[:100]+'(...) '+'\n'

        raw_input('Siguiente...')


