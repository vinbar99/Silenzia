from pymongo import MongoClient
import logging
from ..config import Config

logger = logging.getLogger(__name__)

def init_db():
    try:
        client = MongoClient(Config.MONGO_URI)
        db = client[Config.MONGO_DB_NAME]
        
        # Verifica connessione
        client.server_info()
        
        # Setup indici - gestione errori più robusta
        try:
            # Prima droppo gli indici esistenti per evitare conflitti
            db.users.drop_indexes()
            db.prenotazioni.drop_indexes()
            
            # Ricreo gli indici necessari
            db.users.create_index("username", unique=True)
            db.users.create_index("email", unique=True)
            db.prenotazioni.create_index([("user_id", 1), ("data", 1)], 
                                       unique=True, 
                                       name="idx_user_data_unique")  
            
        except Exception as e:
            logger.warning(f"Errore setup indici (potrebbe essere ok se esistono già): {str(e)}")
            # Continuo comunque, gli indici potrebbero già esistere
        
        logger.info("Connessione DB OK")
        return db
    except Exception as e:
        logger.critical(f"Errore connessione DB: {str(e)}")
        raise

db = init_db()
