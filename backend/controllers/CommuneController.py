from database.DbConfig import DbConfig
from models.Commune import Commune
import os
import geojson
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, func
from shapely.geometry import mapping
from geoalchemy2.shape import to_shape
from geoalchemy2.functions import ST_Transform
import json

class CommuneController:
    def __init__(self):
        self.db = DbConfig()
        self.cursor = self.db.connexion()
        self.engine = create_engine("postgresql://" + os.getenv("PG_USER_BDUNI") + ":" + os.getenv("PG_PASSWORD_BDUNI")+ "@" + os.getenv("PG_HOST_BDUNI")+ ":" + os.getenv("PG_PORT_BDUNI") + "/" + os.getenv("PG_NAME_BDUNI"))
        
    
    def get_communes(self):
        request = self.cursor.execute(f"SELECT nom_officiel, code_insee FROM commune WHERE gcms_detruit=\'false\' ORDER BY nom_officiel")
        rows = self.cursor.fetchall()
        communes = []
        results = [{"nom_commune": row[0], "code_insee": row[1]} for row in rows]
        return results
    
    
    def get_commune_by_code_insee(self, code_insee):
        Session = sessionmaker(bind=self.engine)
        session = Session()
        
        commune_properties = session.query(
        Commune.nom_officiel,
        Commune.cleabs,
        Commune.code_postal,
        Commune.population, 
        Commune.code_insee,
        Commune.code_insee_du_canton,
        Commune.nom_de_la_region,
        Commune.nom_de_l_arrondissement,
        Commune.nom_du_departement,
        Commune.nom_de_la_collectivite_terr,
        Commune.organisme_recenseur,
        Commune.capitale_d_etat,
        Commune.code_siren,
        Commune.gcms_detruit
        
        ).filter(Commune.code_insee == str(code_insee)).first()
        
        commune_geometry = session.query(
        func.ST_Transform(func.ST_SetSRID(Commune.geometrie_ge, 2154), 4326).label('geometrie')
        ).filter(Commune.code_insee == str(code_insee), Commune.gcms_detruit == "false").one()
    
        shape = to_shape(commune_geometry.geometrie)
        
        feature = geojson.Feature(geometry = shape, properties = {
            "nom_officiel" : commune_properties.nom_officiel,
            "cleabs": commune_properties.cleabs,
            "code_postal": commune_properties.code_postal,
            "population" : commune_properties.population,
            "code_insee": commune_properties.code_insee,
            "code_insee_du_canton": commune_properties.code_insee_du_canton,
            "nom_de_la_region" : commune_properties.nom_de_la_region,
            "nom_de_l_arrondissement": commune_properties.nom_de_l_arrondissement,
            "nom_du_departement": commune_properties.nom_du_departement,
            "nom_de_la_collectivite_terr": commune_properties.nom_de_la_collectivite_terr,
            "organisme_recenseur": commune_properties.organisme_recenseur,
            "capitale_d_etat": commune_properties.capitale_d_etat,
            "code_siren": commune_properties.code_siren,
            "gcms_detruit": commune_properties.gcms_detruit
        })

        return feature
        
        """try :
            
        except:
            return {"message": "Cette commune n'existe pas"}"""
