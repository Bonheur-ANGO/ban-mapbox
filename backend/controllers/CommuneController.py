from database.DbConfig import DbConfig
from models.Commune import Commune
import os
import geojson
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from geoalchemy2.shape import to_shape
import json

class CommuneController:
    def __init__(self):
        self.db = DbConfig()
        self.cursor = self.db.connexion()
        self.engine = create_engine("postgresql://" + os.getenv("PG_USER_BDUNI") + ":" + os.getenv("PG_PASSWORD_BDUNI")+ "@" + os.getenv("PG_HOST_BDUNI")+ ":" + os.getenv("PG_PORT_BDUNI") + "/" + os.getenv("PG_NAME_BDUNI"))
        
    
    def get_communes(self):
        request = self.cursor.execute(f"SELECT nom_officiel, code_insee FROM commune ORDER BY nom_officiel")
        rows = self.cursor.fetchall()
        communes = []
        results = [{"nom_commune": row[0], "code_insee": row[1]} for row in rows]
        return results
    
    
    def get_commune_by_code_insee(self, code_insee):
        Session = sessionmaker(bind=self.engine)
        session = Session()
        
        try :
            commune = session.query(Commune).filter(Commune.code_insee == str(code_insee)).one()
        
            shape = to_shape(commune.geometrie)
            
            feature = geojson.Feature(geometry=shape, properties = {
                "nom_officiel" : commune.nom_officiel,
                "cleabs": commune.cleabs,
                "code_postal": commune.code_postal,
                "population" : commune.population,
                "code_insee": commune.code_insee,
                "code_insee_du_canton": commune.code_insee_du_canton,
                "nom_de_la_region" : commune.nom_de_la_region,
                "nom_de_l_arrondissement": commune.nom_de_l_arrondissement,
                "nom_du_departement": commune.nom_du_departement,
                "nom_de_la_collectivite_terr": commune.nom_de_la_collectivite_terr,
                "organisme_recenseur": commune.organisme_recenseur,
                "capitale_d_etat": commune.capitale_d_etat
            })

            return feature
        except:
            return {"message": "Cette commune n'existe pas"}
