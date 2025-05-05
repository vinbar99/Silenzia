from flask import Blueprint, request, render_template, redirect, url_for, flash, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash
import re
from datetime import datetime

from ..core.database import db
from ..core.models import User
from ..core.logging import logger

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/api/auth/login', methods=['GET', 'POST'])
def login():
    # Se GET, mostro form login 
    if request.method == 'GET':
        return render_template('login.html')
        
    # Altrimenti processo POST
    try:
        # Supporta sia JSON che form data
        if request.is_json:
            data = request.get_json()
        else:
            data = request.form
            
        username = data.get('username')
        password = data.get('password')
        
        if not all([username, password]):
            return jsonify({"error": "Username e password richiesti"}), 400

        try:
            # Controllo se utente esiste
            utente = db.users.find_one({"username": username})

            # Check password e login
            if utente and User.validate_login(utente['password'], password):
                user_obj = User(username=utente['username'],
                                email=utente['email'])
                login_user(user_obj)

                # Log per audit
                logger.info(
                    f"Login effettuato: {username} - IP: {request.remote_addr}"
                )

                # Redirect alla pagina prenotazioni dopo login
                next_page = request.args.get('next')
                flash('Login effettuato con successo!', 'success')
                return redirect(next_page if next_page else url_for('prenota'))

            # Password sbagliata - redirect con messaggio
            logger.warning(
                f"Login fallito per {username} - IP: {request.remote_addr}")
            flash('Username o password non validi', 'error')
            return redirect(url_for('auth.login'))

        except Exception as e:
            # Qualcosa è andato storto nel DB
            logger.error(f"Errore login: {str(e)} - User: {username}")
            return jsonify({"error": "Errore di sistema"}), 500

    except Exception as e:
        # Errore nel parsing JSON
        logger.error(f"Errore parsing JSON: {str(e)}")
        return jsonify({"error": "Richiesta malformata"}), 400

    # Se GET, ritorna errore (API REST)
    return jsonify({"error": "Metodo non permesso"}), 405


@auth_bp.route('/api/auth/register', methods=['GET', 'POST']) 
def register():
    # Se GET, mostro form registrazione
    if request.method == 'GET':
        return render_template('register.html')
        
    # Se POST, processo registrazione
    try:
        # Supporta sia JSON che form data
        if request.is_json:
            data = request.get_json()
        else:
            data = request.form
            
        username = data.get('username')
        password = data.get('password') 
        email = data.get('email')

        # Check campi vuoti
        if not all([username, password, email]):
            flash('Tutti i campi sono obbligatori', 'error')
            return redirect(url_for('auth.register'))

        # Validazione dati
        if not re.match(r'^[a-zA-Z0-9_]{3,20}$', username):
            flash(
                'Username non valido (3-20 caratteri, solo lettere, numeri e _)',
                'error')
            return redirect(url_for('auth.register'))

        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
                        email):
            flash('Email non valida', 'error')
            return redirect(url_for('auth.register'))

        if not re.match(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$', password):
            flash(
                'Password troppo debole (min 8 caratteri, almeno 1 lettera e 1 numero)',
                'error')
            return redirect(url_for('auth.register'))

        try:
            # Check se username già preso
            if db.users.find_one({"username": username}):
                flash('Username già in uso', 'error')
                return redirect(url_for('auth.register'))

            # Creo nuovo utente
            nuovo_utente = {
                "username": username,
                "password": generate_password_hash(password),
                "email": email,
                "data_registrazione": datetime.now(),
                "ultimo_accesso": None
            }

            # Salvo su DB
            db.users.insert_one(nuovo_utente)

            # Log registrazione
            logger.info(f"Nuovo utente: {username} - Email: {email}")
            
            # Redirect alla pagina login con messaggio di successo
            flash('Registrazione completata con successo! Ora puoi accedere', 'success')
            return redirect(url_for('auth.login'))

        except Exception as e:
            logger.error(f"Errore registrazione: {str(e)} - User: {username}")
            return jsonify({"error": "Errore durante la registrazione"}), 500

    except Exception as e:
        logger.error(f"Errore parsing JSON: {str(e)}")
        return jsonify({"error": "Richiesta malformata"}), 400


@auth_bp.route('/logout')
@login_required
def logout():
    username = current_user.username
    logout_user()
    logger.info(f"Logout: {username}")
    return redirect(url_for('homepage'))
