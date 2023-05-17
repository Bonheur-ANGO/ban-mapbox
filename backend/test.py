import gzip
from database.DbConfig import DbConfig
from controllers.CommuneController import CommuneController
from controllers.TronconController import TronconController
from helpers.NormalizeStreetName import NormalizeStreetName
from controllers.GeometricMatchingController import GeometricMatchingController
from helpers.JSONConverter import JSONConverter
import pandas as pd

"""file_path = './adresses-01.csv.gz'

with gzip.open(file_path, "rt", encoding="utf-8") as file:
    data= pd.read_csv(file, on_bad_lines='skip')


postal_code = 75001  # Remplacez par le code postal souhaité
filtered_data = data[data['code_postal'] == postal_code]
print(filtered_data)"""

commune = CommuneController()
geo = GeometricMatchingController()

'''for row in geo.get_nearest_troncon("94067"):
    print(row)'''
 
print(geo.get_nearest_troncon("94067"))
    
'''normalize_street_name = NormalizeStreetName()

print(normalize_street_name.format("PAS BIR-HAKEIM"))
'''
