from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import check_password_hash
from ..core.database import db

class User(UserMixin):
    def __init__(self, username, email):
        self.username = username
        self.email = email
        
        # Aggiorno ultimo accesso
        db.users.update_one(
            {"username": username},
            {"$set": {"ultimo_accesso": datetime.now()}}
        )
        
    def get_id(self):
        return self.username
        
    @staticmethod
    def get_by_username(username):
        user_data = db.users.find_one({"username": username})
        if user_data:
            return User(user_data['username'], user_data['email'])
        return None
        
    @staticmethod
    def validate_login(stored_password, provided_password):
        # Check semplice con werkzeug 
        return check_password_hash(stored_password, provided_password)
