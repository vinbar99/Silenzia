from datetime import datetime
from ..core.database import db

class Booking:
    @staticmethod
    def get_user_bookings(username):
        try:
            prenotazioni = list(db.prenotazioni.find(
                {"user_id": username}
            ).sort("data", 1))
            
            # Fix per ObjectId non serializzabile
            for p in prenotazioni:
                p['_id'] = str(p['_id'])
            return prenotazioni
            
        except Exception as e:
            logger.error(f"Errore recupero prenotazioni: {str(e)}")
            return []
            
    @staticmethod
    def validate_booking_time(ora):
        try:
            ora_num = int(ora.split(':')[0])
            return 10 <= ora_num <= 21
        except:
            return False
            
    @staticmethod
    def generate_booking_code():
        """Genera un codice alfanumerico per la prenotazione"""
        import random
        import string
        chars = string.ascii_uppercase + string.digits
        return ''.join(random.choices(chars, k=6))  # codice di 6 caratteri
