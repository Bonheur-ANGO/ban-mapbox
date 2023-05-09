from dotenv import load_dotenv
import psycopg2
import os

class DbConfig:
    def __init__(self):
        load_dotenv()
        self.host = os.getenv("PG_HOST_BDUNI")
        self.database = os.getenv("PG_NAME_BDUNI")
        self.user = os.getenv("PG_USER_BDUNI")
        self.password = os.getenv("PG_PASSWORD_BDUNI")
        self.port = os.getenv("PG_PORT_BDUNI")
    
    def connexion(self):
        try:
            conn = psycopg2.connect(host=self.host, database=self.database, user=self.user, password=self.password)
            return conn.cursor()
        except:
            print("Erreur de connexion à la base de donnée")