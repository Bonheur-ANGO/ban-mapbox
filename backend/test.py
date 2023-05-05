import gzip
import pandas as pd

file_path = './adresses-01.csv.gz'

with gzip.open(file_path, "rt", encoding="utf-8") as file:
    data= pd.read_csv(file, on_bad_lines='skip')


postal_code = 75001  # Remplacez par le code postal souhaité
filtered_data = data[data['code_postal'] == postal_code]
print(filtered_data)
