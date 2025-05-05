from flask import Flask, render_template
from flask_login import LoginManager, login_required
from flask_cors import CORS
from datetime import timedelta
import logging

from .core.database import init_db
from .core.logging import setup_logger
from .core.models import User
from .config import Config

def create_app():
    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    app.config.from_object(Config)
    
    # Setup
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    setup_logger()
    
    # Login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = "Devi fare il login per accedere"
    
    @login_manager.user_loader
    def load_user(username):
        return User.get_by_username(username)
        
    # Registra blueprints
    from .auth.routes import auth_bp
    from .booking.routes import booking_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(booking_bp)
    
    # Route principali
    @app.route('/')
    def homepage():
        return render_template('homepage.html')
        
    @app.route('/prenota')
    @login_required  # protezione route prenotazione
    def prenota():
        return render_template('index.html')  # pagina prenotazioni
        
    @app.route('/info')
    def info():
        return render_template('info.html')
        
    @app.route('/contatti') 
    def contatti():
        return render_template('contatti.html')
    
    return app
