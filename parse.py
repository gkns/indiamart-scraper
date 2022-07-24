# For people having a look, Ignore the identation in this file,
# I know it doesn't look the best,
# But this is a quick and dirty script to get the job done.


from selenium import webdriver
from bs4 import BeautifulSoup
from collections import defaultdict
from selenium.webdriver.firefox.options import Options

import os
import json
import csv
import re

class Scraper():
    def __init__(self):
        self.product_link_list = []
        self.image_links = {}
        self.products_map_fields = ['name', 'price', 'details', 'description', 'image']
        self.products = []

    def get_products_in_page(self):
        options = Options()
        options.headless = True
        self.browser=webdriver.Firefox(options=options)

        with open('products_link.list', 'r') as prod_link_list_file:
            for page in prod_link_list_file:
                self.browser.get(page)
                soup=BeautifulSoup(self.browser.page_source)
                prods = soup.find_all('div', class_='FM_prdpge')
                for prod in prods:
                    product = {}
                    name_elem = prod.find('h2', class_='FM_f22')
                    product['name'] = name_elem.text

                    print ('Parsing product: ' + name_elem.text)
                    
                    price_elem = prod.find('p', class_='FM_f18')
                    if price_elem:
                        price = price_elem.text.split('/')[0].strip()
                        product['price'] = price
                    else:
                        product['price'] = ''
                    
                    desc_elem = prod.find('div', class_='lh28')
                    tds = [row.find_all('td') for row in desc_elem.find_all('tr')]
                    results = { td[0].text: td[1].text for td in tds if len(td) == 2}
                    product['details'] = results
                    for string in desc_elem.stripped_strings:
                        product['description'] = string
                    
                    img_elem = prod.find('img', class_='FM_ps_b')
                    if img_elem:
                        product['image'] = img_elem['src']

                    self.products.append(product)


            with open('data.csv', 'w') as csvfile:
                csvwriter = csv.DictWriter(csvfile, fieldnames=self.products_map_fields)
                csvwriter.writeheader()
                for prod in self.products:
                    csvwriter.writerow(prod)

    def main(self):
        try:
            self.get_products_in_page()
        finally:
            if self.browser:
                self.browser.close()
                self.browser.quit()

if __name__ == "__main__":
    Scraper().main()