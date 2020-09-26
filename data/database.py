# import mysql.connector
# from mysql.connector import Error
import requests
import random
import sys
import io
import re
# import time

class api():

    def __init__(self):
        # api-endpoint 
        self.list_product = []
        self.url = "https://fr.openfoodfacts.org/cgi/search.pl"

    def get_info_from_api(self, categories, index):

        self.payload = {
        "tag_0": "categories",
            "tag_contains_0": "contains",
            "tagtype_0": "categories",
            "sort_by": "unique_scans_n",
            "page": 1,
            "page_size": 20,
            "action": "process",
            "json": 1
        }
        print(
                'Récuperation des données à partir de l api pour la catégorie:'
                + ' ' + categories
                )
        self.list_product = []
        # self.counter = 1
        for c in range(1,2,1): # 5 pages
            self.payload['page'] = c
            self.payload['tag_0'] = categories
            for j in range(1, 19, 1): #  20 resultats par pages
                # self.payload['tag_0'] = i
                # print('-----------')
                # print(j)
                # time.sleep(1)
                # self.payload['page'] = self.counter #  nombre de pages
                self.r = requests.get(
                    url = self.url,
                    params = self.payload,
                    headers = {
                        'UserAgent':
                        'Project OpenFood - MacOS - Version 10.13.6'
                        }
                )
                self.data = self.r.json()
                # print(self.data)
                # time.sleep(1)

                if not 'nutriscore_grade' in self.data['products'][j]:
                    self.data['products'][j]['nutriscore_grade'] = 'na'
                if not 'ingredients_text_fr' in self.data['products'][j]:
                    self.data['products'][j]['ingredients_text_fr'] = 'na'
                if not 'stores_tags' in self.data['products'][j]:
                    self.data['products'][j]['stores_tags'] = 'na'
                self.list_product.append(
                    (self.data['products'][j]['code'],
                    index,
                    self.data['products'][j]['product_name'],
                    self.data['products'][j]['url'],
                    self.data['products'][j]['stores_tags'],
                    self.data['products'][j]['ingredients_text_fr'],
                    self.data['products'][j]['nutriscore_grade']
                    )

                )
    
        return(self.list_product)