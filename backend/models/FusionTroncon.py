from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from geoalchemy2 import Geometry

Base = declarative_base()

class FusionTroncon:
    __tablename__ = "troncon_de_route"
    identifiant_voie = Column(String)
    nom_minuscule = Column(String)
    nom_initial_troncon = Column(String)
    geometrie = Column(Geometry("POINT"))