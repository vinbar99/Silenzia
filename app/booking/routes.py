from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from datetime import datetime
from bson import ObjectId

from ..core.database import db
from ..core.logging import logger
from .models import Booking

booking_bp = Blueprint('booking', __name__, url_prefix='/api')

@booking_bp.route('/prenotazioni', methods=['GET'])
@login_required
def get_bookings():
    try:
        bookings = Booking.get_user_bookings(current_user.username)
        return jsonify({"prenotazioni": bookings})
    except Exception as e:
        logger.error(f"Errore recupero prenotazioni: {str(e)}")
        return jsonify({"errore": "Impossibile recuperare prenotazioni"}), 500

@booking_bp.route('/prenotazioni', methods=['POST'])
@login_required
def create_booking():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"errore": "Dati prenotazione mancanti"}), 400
            
        # Check campi obbligatori
        required = ['nome', 'cognome', 'email', 'data', 'ora', 'persone']
        missing = [f for f in required if not data.get(f)]
        if missing:
            return jsonify({"errore": f"Campi obbligatori mancanti: {', '.join(missing)}"}), 400
            
        # Aggiungi user_id e codice   
        data['user_id'] = current_user.username
        data['codice'] = Booking.generate_booking_code()
        
        try:
            # Prova inserimento
            result = db.prenotazioni.insert_one(data)
            booking = db.prenotazioni.find_one({"_id": result.inserted_id})
            booking["_id"] = str(booking["_id"])
            return jsonify(booking)
            
        except Exception as e:
            if "duplicate key error" in str(e):
                return jsonify({
                    "errore": f"Hai già una prenotazione per il {data['data']}"
                }), 400
            raise
            
    except Exception as e:
        logger.error(f"Errore creazione prenotazione: {str(e)}")
        return jsonify({"errore": "Errore del server, riprova più tardi"}), 500

@booking_bp.route('/prenotazioni/<id>', methods=['PUT'])
@login_required
def update_booking(id):
    try:
        data = request.get_json()
        if not data:
            return jsonify({"errore": "Dati non validi"}), 400

        # Aggiorna prenotazione
        booking = db.prenotazioni.find_one_and_update(
            {"_id": ObjectId(id), "user_id": current_user.username},
            {"$set": data},
            return_document=True
        )

        if not booking:
            return jsonify({"errore": "Prenotazione non trovata"}), 404

        # Fix ObjectId per JSON
        booking["_id"] = str(booking["_id"])
        return jsonify(booking)

    except Exception as e:
        logger.error(f"Errore modifica prenotazione: {str(e)}")
        return jsonify({"errore": "Impossibile modificare la prenotazione"}), 500

@booking_bp.route('/prenotazioni/<id>', methods=['DELETE'])
@login_required
def delete_booking(id):
    try:
        # Cancella solo se l'utente è proprietario
        result = db.prenotazioni.delete_one({
            "_id": ObjectId(id),
            "user_id": current_user.username
        })

        if result.deleted_count == 0:
            return jsonify({"errore": "Prenotazione non trovata"}), 404

        return jsonify({"message": "Prenotazione cancellata"})

    except Exception as e:
        logger.error(f"Errore cancellazione prenotazione: {str(e)}")
        return jsonify({"errore": "Impossibile cancellare la prenotazione"}), 500