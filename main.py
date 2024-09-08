from app import create_app
from db_setup import create_database

app = create_app()

if __name__ == '__main__':
    create_database()
    app.run(debug=True)