import os
from datetime import timedelta  # aggiunto per PERMANENT_SESSION_LIFETIME

from dotenv import load_dotenv
import os

# Carica variabili da .env
load_dotenv()

class Config:
    # Usa getenv con fallback per dev/test
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key-non-sicura')
    PERMANENT_SESSION_LIFETIME = timedelta(hours=2)
    
    # MongoDB - prendi credenziali da env
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017')
    MONGO_DB_NAME = os.getenv('MONGO_DB_NAME', 'silenzia_dev')
    
    # App config
    BOOKING_MAX_PER_DAY = 2
    BOOKING_HOURS = (10, 21)  # Orario 10-21
