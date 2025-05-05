
# Architettura Silenzia


## Overview
Il sistema è strutturato secondo il pattern MVC utilizzando Flask come framework principale. La struttura delle cartelle riflette questa separazione:

```
app/
├── api/         # API REST 
├── auth/        # Gestione autenticazione
├── booking/     # Logica prenotazioni
└── core/        # Componenti di base
```

## Componenti Principali

### Frontend
- Template HTML in `/templates`
- Stili CSS in `static/style.css` 
- JavaScript in `static/script.js`
- Assets in `static/img/`

### Backend 
- Entry point: `main.py`
- Blueprint auth: `app/auth/routes.py`
- Blueprint booking: `app/booking/routes.py`
- Modelli dati: `app/core/models.py`

### Database
MongoDB per la persistenza dei dati, configurato in `app/core/database.py`

## Sicurezza
- Password hashate (implementato in User model)
- Protezione CSRF attiva
- Login richiesto per prenotazioni
- Validazione input lato client e server

## Note Sviluppatore su replit
Per avviare in development:
```bash
python main.py  # Avvia server debug su porta 5000
```

Per dettagli implementativi vedere i singoli moduli.
