# -*- coding: utf-8 -*-
"""
Created on Fri Sep 14 09:57:33 2018

@author: Javier
"""

#%%
from requests import get
from bs4 import BeautifulSoup
import sys
import urllib2
# just randomly picking an encoding.... a command line param may be
# useful if you want to get input from files
_stdin_encoding = sys.stdin.encoding or 'utf-8'

def unicode_input(prompt):
    return raw_input(prompt).decode('latin1')


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

product_containers = html_soup.find_all('p', class_ = 'product-info-description')
quantity = len(product_containers)
print('he encontrado '+str(quantity)+' resultados')

