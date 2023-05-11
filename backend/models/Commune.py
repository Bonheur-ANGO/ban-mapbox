from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from geoalchemy2 import Geometry
from geoalchemy2.shape import to_shape


Base = declarative_base()

class Commune(Base):
    __tablename__ = "commune"
    cleabs = Column(String, primary_key=True)
    code_insee = Column(String)
    code_insee_du_canton = Column(String)
    code_insee_de_l_arrondissement = Column(String)
    code_insee_de_la_collectivite_terr = Column(String)
    code_insee_du_departement = Column(String)
    code_insee_de_la_region = Column(String)
    population = Column(String)
    surface_en_ha = Column(String)
    gcms_detruit = Column(String)
    gcms_date_creation = Column(String)
    gcms_date_modification = Column(String)
    gcms_date_destruction = Column(String)
    date_d_apparition = Column(String)
    date_de_confirmation = Column(String)
    diffusion = Column(String)
    complement = Column(String)
    code_postal = Column(String)
    nom_officiel = Column(String)
    ancien_nom = Column(String)
    nom_de_l_arrondissement = Column(String)
    nom_de_la_collectivite_terr = Column(String)
    nom_du_departement = Column(String)
    nom_de_la_region = Column(String)
    chef_lieu_d_arrondissement = Column(String)
    
    chef_lieu_de_collectivite_terr = Column(String)
    chef_lieu_de_departement = Column(String)
    chef_lieu_de_region = Column(String)
    
    capitale_d_etat = Column(String)
    date_du_recensement = Column(String)
    organisme_recenseur = Column(String)
    codes_siren_des_epci = Column(String)
    
    nom = Column(String)
    commentaire_centralise = Column(String)
    commentaire_collecteur = Column(String)
    
    lien_vers_chef_lieu = Column(String)
    liens_vers_autorite_administrative = Column(String)
    gcms_numrec = Column(String)
    
    gcms_territoire = Column(String)
    gcms_fingerprint = Column(String)
    gcvs_nom_lot = Column(String)
    exception_legitime = Column(String)
    
    code_siren = Column(String)
    gcvs_empreinte = Column(String)

    geometrie_ge = Column(Geometry(geometry_type="POLYGON"))