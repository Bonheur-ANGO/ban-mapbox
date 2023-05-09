from database.DbConfig import DbConfig
import json

class CommuneController:
    def __init__(self):
        self.db = DbConfig()
        self.cursor = self.db.connexion()
        
    
    def get_communes(self):
        request = self.cursor.execute(f"SELECT nom_officiel FROM commune ORDER BY nom_officiel")
        rows = self.cursor.fetchall()
        communes = []
        results = [{"nom_commune": row[0]} for row in rows]
        return results

