import gzip
from database.DbConfig import DbConfig
import requests
from controllers.CommuneController import CommuneController
from controllers.TronconController import TronconController
from helpers.NormalizeStreetName import NormalizeStreetName
from controllers.GeometricMatchingController import GeometricMatchingController
from helpers.JSONConverter import JSONConverter
import pandas as pd
import os
import urllib3


os.environ['http_proxy'] = "http:proxy//ign.fr:3128"

current_dir = os.path.dirname(__file__)
csv_path = os.path.join(current_dir, 'ressources/commune.csv')
url = "https://api-adresse.data.gouv.fr/search/csv/"

proxies = {
  "http": "http://proxy.ign.fr:3128",
  "https": "http://proxy.ign.fr:3128",
}

'''with open(csv_path, 'rb') as f:
    files = {'data': f}
    response = requests.post(url, files=files, proxies=proxies)

# Vérifiez que la requête a réussi
if response.status_code == 200:
    # Les résultats sont retournés en format CSV dans la réponse
    result_csv = response.text
    print(result_csv)
else:
    print(f'Erreur lors de la requête: {response.status_code}')'''



'''postal_code = 75001  # Remplacez par le code postal souhaité
filtered_data = data[data['code_postal'] == postal_code]
print(filtered_data)'''

#commune = CommuneController()
#geo = GeometricMatchingController()

'''for row in geo.get_nearest_troncon("94067"):
    print(row)'''
 
#print(geo.get_nearest_troncon("94067"))
    
'''normalize_street_name = NormalizeStreetName()

print(normalize_street_name.format("PAS BIR-HAKEIM"))
'''
gm = GeometricMatchingController()

print(gm.get_line_adress_by_voie('94067'))