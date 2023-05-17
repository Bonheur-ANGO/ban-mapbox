import re
import os
import pandas as pd

class NormalizeStreetName:
    def __init__(self):
        current_dir = os.path.dirname(__file__)
        csv_path = os.path.join(current_dir, '../ressources/abbreviations.csv')
        csv = pd.read_csv(csv_path, delimiter=";")
        self.abbreviations = dict(zip(csv['txt_court'], csv['txt_long']))
    
    def format(self, name : str):
        for abbr, full in self.abbreviations.items():
            if pd.isna(abbr) or pd.isna(full):
                continue
            
            name = re.sub(r'\b'+re.escape(abbr)+r'\b', full, name, flags=re.IGNORECASE).upper()

        
        return name
            
