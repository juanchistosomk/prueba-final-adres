import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    
    DATABASE = os.path.join(os.getcwd(), 'prueba_adres.db')    
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{DATABASE}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'pf_adress_secret_key_123')