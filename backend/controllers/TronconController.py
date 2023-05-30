from database.DbConfig import DbConfig
from models.Commune import Commune
from models.Troncon import Troncon
import os
from shapely import wkt
import geojson
from geoalchemy2.shape import to_shape
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, func, text

class TronconController:
    def __init__(self):
        self.engine = create_engine("postgresql://" + os.getenv("PG_USER_BDUNI") + ":" + os.getenv("PG_PASSWORD_BDUNI")+ "@" + os.getenv("PG_HOST_BDUNI")+ ":" + os.getenv("PG_PORT_BDUNI") + "/" + os.getenv("PG_NAME_BDUNI"))
    
    
    