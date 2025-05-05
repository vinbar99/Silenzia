from app import create_app

# Entry point dell'applicazione
app = create_app()

if __name__ == '__main__':
    # Debug mode per sviluppo locale (Utilizzato su REPLIT)
    app.run(host='0.0.0.0', port=5000, debug=True)
