from database.DbConfig import DbConfig
from models.Commune import Commune
from models.Troncon import Troncon
import os
import geojson
from geoalchemy2.shape import to_shape
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, func

class TronconController:
    def __init__(self):
        self.engine = create_engine("postgresql://" + os.getenv("PG_USER_BDUNI") + ":" + os.getenv("PG_PASSWORD_BDUNI")+ "@" + os.getenv("PG_HOST_BDUNI")+ ":" + os.getenv("PG_PORT_BDUNI") + "/" + os.getenv("PG_NAME_BDUNI"))
    
    
    def get_all_troncon(self, code_insee):
        Session = sessionmaker(bind=self.engine)
        session = Session()
        troncons = session.query(
            Troncon.cleabs,
            Troncon.nature,
            Troncon.insee_commune_gauche,
            Troncon.insee_commune_droite,
            Troncon.type_d_adressage_du_troncon,
            Troncon.code_postal_droit,
            Troncon.code_postal_gauche,
            func.ST_Transform(func.ST_SetSRID(Troncon.geometrie, 2154), 4326).label('geometrie')
            ).filter(Troncon.insee_commune_droite == str(code_insee) or Troncon.insee_commune_gauche == str(code_insee)).all()
        
        
        features = []
        
        for troncon in troncons:
            shape = to_shape(troncon.geometrie)
            feature = geojson.Feature(geometry=shape, properties={
            "cleabs" : troncon.cleabs,
            "nature": troncon.nature,
            "type_d_adressage_du_troncon": troncon.type_d_adressage_du_troncon,
            "code_postal_droit": troncon.code_postal_droit,
            "code_postal_gauche": troncon.code_postal_gauche,
            "insee_commune_gauche": troncon.insee_commune_gauche,
            "insee_commune_droite": troncon.insee_commune_droite
            })
            features.append(feature)
            feature_collection = geojson.FeatureCollection(features)
        return feature_collection