
# Analisi dei Requisiti - Silenzia


## Requisiti Funzionali

### RF1. Gestione Utenti
- RF1.1 Registrazione nuovo utente con email, username e password
- RF1.2 Login utente registrato
- RF1.3 Logout dalla sessione corrente

### RF2. Gestione Prenotazioni
- RF2.1 Visualizzazione calendario disponibilità
- RF2.2 Creazione nuova prenotazione
- RF2.3 Modifica prenotazione esistente
- RF2.4 Cancellazione prenotazione
- RF2.5 Visualizzazione storico prenotazioni personali

### RF3. Sistema Accessi
- RF3.1 Generazione codice univoco per ogni prenotazione
- RF3.2 Verifica codice per accesso cabina

## Requisiti Non Funzionali

### RNF1. Prestazioni
- Tempo di risposta < 2 secondi per operazioni standard
- Gestione contemporanea di almeno 100 utenti attivi

### RNF2. Sicurezza
- Crittografia password (hash + salt)
- Protezione da SQL injection
- Validazione input lato client e server
- Sessioni con timeout dopo 2 ore

### RNF3. Usabilità
- Interface responsive (mobile-first)
- Feedback chiaro per ogni azione utente

### RNF4. Affidabilità
- Backup giornaliero database
- Disponibilità sistema 99.9%
- Gestione errori robusta


