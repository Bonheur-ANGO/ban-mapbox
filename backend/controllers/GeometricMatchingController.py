from database.DbConfig import DbConfig
from models.Commune import Commune
import os
import geojson
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, text


class GeometricMatchingController:
    def __init__(self) :
        self.db = DbConfig()
        self.cursor = self.db.connexion()
        self.engine = create_engine("postgresql://" + os.getenv("PG_USER_BDUNI") + ":" + os.getenv("PG_PASSWORD_BDUNI")+ "@" + os.getenv("PG_HOST_BDUNI")+ ":" + os.getenv("PG_PORT_BDUNI") + "/" + os.getenv("PG_NAME_BDUNI"))
        
    
    def get_nearest_troncon(self, code_insee):
        Session = sessionmaker(bind=self.engine)
        session = Session()
        sql = text(f"""
                    WITH distances AS (
                        SELECT a.numero AS numero_adresse, a.insee_commune, a.nom_voie, t.cleabs AS troncon_id, ST_Distance(a.geometrie, t.geometrie) AS distance
                        FROM adresse_ban a
                        JOIN troncon_de_route t
                        ON a.insee_commune = t.insee_commune_gauche AND a.insee_commune = t.insee_commune_droite
                        WHERE a.insee_commune = \'{code_insee}\' AND a.nom_voie='Avenue Pasteur' AND a.gcms_detruit='false'
                    ), min_distances AS (
                        SELECT numero_adresse, nom_voie, insee_commune, MIN(distance) AS min_distance
                        FROM distances
                        GROUP BY numero_adresse, nom_voie, insee_commune
                    )
                    SELECT distances.insee_commune, distances.numero_adresse, distances.troncon_id, distances.nom_voie, distances.distance
                    FROM distances
                    JOIN min_distances
                    ON distances.insee_commune = min_distances.insee_commune
                    AND distances.numero_adresse = min_distances.numero_adresse
                    AND distances.distance = min_distances.min_distance;
                    """)
        result = session.execute(sql)
        return result