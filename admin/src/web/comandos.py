from src.core import seeds
from src.core import database

def register(app):
    @app.cli.command("reset-db")
    def reset_db():
        database.reset()

    @app.cli.command("seed-db") 
    def seed_db():
        seeds.run()
        print("Base de datos sembrada")