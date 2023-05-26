from database.DbConfig import DbConfig
from shapely import wkt, wkb
from shapely.geometry import LineString, Point, shape, mapping
from models.Commune import Commune
from models.FusionTroncon import FusionTroncon
import os
import json
from shapely.ops import nearest_points
from controllers.CommuneController import CommuneController
from helpers.NormalizeStreetName import NormalizeStreetName
import geojson
import geopandas as gpd
from geoalchemy2.shape import to_shape
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, text
from collections import defaultdict


class GeometricMatchingController:
    def __init__(self) :
        self.db = DbConfig()
        self.cursor = self.db.connexion()
        self.commune_ctrl = CommuneController()
        self.engine = create_engine("postgresql://" + os.getenv("PG_USER_BDUNI") + ":" + os.getenv("PG_PASSWORD_BDUNI")+ "@" + os.getenv("PG_HOST_BDUNI")+ ":" + os.getenv("PG_PORT_BDUNI") + "/" + os.getenv("PG_NAME_BDUNI"))
        
    
    def get_nearest_troncon(self, code_insee):
        Session = sessionmaker(bind=self.engine)
        session = Session()
        sql = text(f"""
                    WITH distances AS (
                        SELECT a.cleabs AS adresse_id, a.numero AS numero_adresse, t.nom_1_gauche AS nom_voie_gauche, ST_AsText(ST_Transform(ST_SetSRID(ST_ClosestPoint(t.geometrie, a.geometrie), 2154), 4326)) AS closest_point_on_troncon, ST_AsText(ST_Transform(ST_SetSRID(a.geometrie, 2154), 4326)) AS geometrie_adresse_ban , v.nom_initial_troncon, a.nom_commune, a.suffixe, a.insee_commune, a.nom_voie AS nom_voie_adresse_ban, t.cleabs AS troncon_id, ST_Distance(a.geometrie, t.geometrie) AS distance
                        FROM adresse_ban a
                        JOIN troncon_de_route t
                        ON a.insee_commune = t.insee_commune_gauche OR a.insee_commune = t.insee_commune_droite
                        JOIN voie v
                        ON v.id_pseudo_fpb = t.identifiant_voie_1_gauche OR v.id_pseudo_fpb = t.identifiant_voie_1_droite
                        WHERE a.insee_commune = \'{code_insee}\' AND a.nom_voie= 'Avenue Pasteur' AND a.gcms_detruit='false'
                    ), min_distances AS (
                            SELECT adresse_id, numero_adresse, nom_voie_adresse_ban, MIN(distance) AS min_distance, insee_commune, nom_commune
                            FROM distances
                            GROUP BY adresse_id, numero_adresse, nom_voie_adresse_ban, insee_commune, nom_commune, suffixe
                    )
                    SELECT distances.adresse_id, distances.numero_adresse, distances.suffixe, distances.nom_voie_adresse_ban, distances.nom_commune, distances.nom_initial_troncon, distances.insee_commune, distances.troncon_id, distances.distance, distances.closest_point_on_troncon, distances.geometrie_adresse_ban
                    FROM distances
                    JOIN min_distances
                    ON distances.insee_commune = min_distances.insee_commune AND distances.numero_adresse = min_distances.numero_adresse AND distances.distance = min_distances.min_distance
                    """)
        result = session.execute(sql)
        normalize_street_name = NormalizeStreetName() 
        columns = result.keys()
        features = []
        for obj in result.fetchall():
            data = dict(zip(columns, obj))
            nom_voie_troncon = normalize_street_name.format(data['nom_initial_troncon'])
            nom_voie_adresse_ban = normalize_street_name.format(data['nom_voie_adresse_ban'])
            
            if(nom_voie_adresse_ban != nom_voie_troncon):
                coords_ban_address = wkt.loads(data['geometrie_adresse_ban'])
                coords_troncon = wkt.loads(data['closest_point_on_troncon'])
                #nearest_point_on_troncon = nearest_points(coords_ban_address, coords_troncon)[1]
                line = LineString([coords_ban_address, coords_troncon])
                feature = geojson.Feature(geometry=line, properties={
                    "adresse_id_ban" : data['adresse_id'],
                    "nom_voie_adresse_ban" : nom_voie_adresse_ban,
                    "nom_voie_troncon" : nom_voie_troncon,
                    "troncon_id" : data['troncon_id'],
                    "insee_commune": data['insee_commune'],
                    "nom_commune": data['nom_commune']
                })
                features.append(feature)
        feature_collection = geojson.FeatureCollection(features)
        return feature_collection
    
    def getTronconsFusionned(self, code_insee):
        '''commune_ctrl = CommuneController()
        adresses = commune_ctrl.get_all_adress_by_commune(94067)
        adresses_gpd = gpd.GeoDataFrame.from_features(adresses)
        groupes = adresses_gpd.groupby('nom_voie')'''
        Session = sessionmaker(bind=self.engine)
        session = Session()
        sql = text(f"""
                   SELECT v.cleabs AS identifiant_voie, type_voie, v.nom_minuscule, v.nom_initial_troncon, ST_AsText(ST_Transform(ST_SetSRID(ST_LineMerge(ST_Union(t.geometrie)), 2154),4326)) AS geometrie, t.gcms_detruit
                    FROM voie v
                    JOIN troncon_de_route t
                    ON v.id_pseudo_fpb = t.identifiant_voie_1_gauche OR v.id_pseudo_fpb = t.identifiant_voie_1_droite
                    WHERE v.code_insee =\'{code_insee}\' AND t.gcms_detruit = 'false' AND v.gcms_detruit = 'false'
                    GROUP BY v.cleabs, t.gcms_detruit
                    ORDER BY nom_minuscule



                   """)
        
        result = session.execute(sql)
        columns = result.keys()
        features = []
        for obj in result.fetchall():
            data = dict(zip(columns, obj))
            shape = wkt.loads(data['geometrie'])
            feature = geojson.Feature(geometry=shape, properties={
                "nom_initial_troncon": data['nom_initial_troncon'],
                "nom_minuscule": data['nom_minuscule'],
                "identifiant_voie": data['identifiant_voie'],
                "type_voie": data['type_voie'],
            })
            features.append(feature)
        return features
        
    
    def get_line_adress_by_voie(self, code_insee):
        geojson_data = self.commune_ctrl.get_all_adress_by_commune(code_insee)

        # Group features by street name
        features_by_voie = defaultdict(list)
        for feature in geojson_data['features']:
            features_by_voie[feature['properties']['nom_voie']].append(feature)

        # Create a line for each street using the points of each feature
        lines = []
        for voie, features in features_by_voie.items():
            points = [shape(feature['geometry']) for feature in features]
            if len(points) > 1:
                line = LineString(points)
                lines.append(geojson.Feature(geometry=mapping(line), 
                                            properties={'nom_voie': voie}))

        # Return a feature collection with the lines
        return geojson.FeatureCollection(lines)
        