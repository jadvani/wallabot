# -*- coding: utf-8 -*-
import commonFunctions.py
import BeautifulSoup
import matplotlib.pyplot as plt #%matplotlib inline para que vaya saliendo
from requests import get
url = 'https://es.wallapop.com/search?kws='+commonFunctions.getSearchInput()+'&catIds=&verticalId='
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
        img=commonFunctions.url_to_image(product_images[x]['src'])
        plt.imshow(img)
        plt.show()
        print product_titles[x].get_text()+'->'+product_prices[x].get_text()+'\n'
        print product_descriptions[x].get_text()[:100]+'(...) '+'\n'
        raw_input('Siguiente...')
