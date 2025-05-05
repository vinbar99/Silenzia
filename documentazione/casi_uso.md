
# Casi d'Uso - Silenzia


## CU1: Registrazione Utente 
**Attore:** Cliente non registrato

**Flusso principale:**
1. Cliente accede a `/register`
2. Compila form con username/email/password
3. Sistema valida input (routes.py)
4. Crea account se dati validi
5. Redirect a login

**Eccezioni:**
- Username duplicato
- Dati non validi
- Errori DB

## CU2: Login
**Attore:** Cliente registrato

**Flusso principale:**
1. Accesso a `/login`
2. Inserimento credenziali
3. Validazione (auth/routes.py)
4. Creazione sessione
5. Redirect a prenotazioni

## CU3: Gestione Prenotazioni
**Attore:** Cliente autenticato

**Flusso principale:**
1. Accesso a `/prenota`
2. Visualizza calendario
3. Seleziona slot
4. Conferma prenotazione
5. Riceve codice accesso
6. Modifica prenotazione
7. Cancella prenotazione

Implementato in `booking/routes.py` e `booking/models.py`.

Per dettagli tecnici vedere codice sorgente nelle rispettive cartelle.
