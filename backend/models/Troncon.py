from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from geoalchemy2 import Geometry

Base = declarative_base()

class Troncon(Base):
    __tablename__ = "troncon_de_route"
    
    cleabs = Column(String, primary_key=True)
    nature = Column(String)
    type_d_adressage_du_troncon = Column(String)
    insee_commune_gauche = Column(String)
    insee_commune_droite = Column(String)
    code_postal_droit = Column(String)
    code_postal_gauche = Column(String)
    insee_commune_gauche = Column(String)
    insee_commune_droite = Column(String)
    geometrie = Column(Geometry("POINT"))