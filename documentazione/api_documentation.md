# Silenzia API Documentation

## Authentication APIs

### Login
POST `/api/auth/login`

**Request Body:**
```json
{
  "username": "mario_rossi",
  "password": "password123"
}
```

**Response (200):**
```json
{
  "message": "Login effettuato",
  "user": {
    "username": "mario_rossi",
    "email": "mario@example.com"
  }
}
```

**Error Response (400):**
```json
{
  "error": "Username e password richiesti"
}
```

### Register
POST `/api/auth/register`

**Request Body:**
```json
{
  "username": "mario_rossi",
  "email": "mario@example.com",
  "password": "password123"
}
```

**Response (201):**
```json
{
  "message": "Registrazione completata",
  "user": {
    "username": "mario_rossi",
    "email": "mario@example.com"
  }
}
```

## Authentication
tutti gli endpoints richiedono Bearer token authentication:
```
Authorization: Bearer <your_token>
```

## Endpoints

### List Bookings
GET `/prenotazioni`

Recupera tutte le prenotazioni per l'utente autenticato.

**Response Codes:**
- 200: Success
- 401: Unauthorized
- 500: Server Error

**Response Example:**
```json
{
  "prenotazioni": [
    {
      "id": "6457b3e12c7b9a8f3e1d4a2b",
      "nome": "Mario",
      "cognome": "Rossi",
      "email": "mario@example.com",
      "data": "2025-05-10",
      "ora": "14:30",
      "persone": 2,
      "codice": "ABC123",
      "user_id": "mario_username"
    }
  ]
}
```

### Create Booking
POST `/prenotazioni`

Crea prenotazione.

**Request Body:**
```json
{
  "nome": "Mario",
  "cognome": "Rossi",
  "email": "mario@example.com",
  "data": "2025-05-10",
  "ora": "14:30",
  "persone": 2
}
```

**Response Codes:**
- 201: Created
- 400: Bad Request
- 401: Unauthorized
- 500: Server Error

**Response Example:**
```json
{
  "id": "6457b3e12c7b9a8f3e1d4a2b",
  "nome": "Mario",
  "cognome": "Rossi",
  "email": "mario@example.com",
  "data": "2025-05-10",
  "ora": "14:30",
  "persone": 2,
  "codice": "ABC123",
  "user_id": "mario_username"
}
```

### Update Booking
PUT `/prenotazioni/{id}`

Aggiorna una prenotazione esistente.

**Parameters:**
- id: Booking ID (string)

**Request Body:**
```json
{
  "persone": 3,
  "ora": "15:30"
}
```

**Response Codes:**
- 200: Success
- 400: Bad Request
- 401: Unauthorized
- 404: Not Found
- 500: Server Error

**Response Example:**
```json
{
  "id": "6457b3e12c7b9a8f3e1d4a2b",
  "nome": "Mario",
  "cognome": "Rossi",
  "email": "mario@example.com",
  "data": "2025-05-10",
  "ora": "15:30",
  "persone": 3,
  "codice": "ABC123",
  "user_id": "mario_username"
}
```

### Delete Booking
DELETE `/prenotazioni/{id}`

Elimina una premotazione.

**Parameters:**
- id: Booking ID (string)

**Response Codes:**
- 200: Success
- 401: Unauthorized
- 404: Not Found
- 500: Server Error

**Response Example:**
```json
{
  "message": "Prenotazione cancellata"
}
```

## Error Responses
tutti gli errori seguiranno questo formato:
```json
{
  "errore": "Descrizione dell'errore"
}
```