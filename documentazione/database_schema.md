
# Schema Database MongoDB

## Collezione: users
```
{
  username: String (unique, required),
  email: String (unique, required),
  password: String (hashed, required),
  ultimo_accesso: Date
}
```

## Collezione: prenotazioni 
```
{
  _id: ObjectId,
  user_id: String (required),
  nome: String (required),
  cognome: String (required),
  email: String (required),
  data: Date (required),
  ora: String (required),
  persone: Number (required),
  codice: String (required, 6 caratteri alfanumerici)
}
```

### Indici
- users.username (unique)
- users.email (unique)
- prenotazioni.user_id
- prenotazioni.data
- prenotazioni.[user_id, data] (unique, compound)

