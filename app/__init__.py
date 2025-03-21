from flask import Flask, g
from flask_restx import Api  
import os
from app.db import get_db

def create_app():

    app = Flask(__name__)
      
    # Configuración general
    app.config.from_object('config.Config')


    def init_db():
        with app.app_context():
            db = get_db()            
            with app.open_resource('../schema.sql', mode='r', encoding="utf-8") as f:
                db.cursor().executescript(f.read())
            db.commit()
                  

    # Crea la BD si no existe
    if not os.path.exists(app.config['DATABASE']):
        init_db()

    # Cierra conexión a la BD automáticamente
    @app.teardown_appcontext
    def close_db_connection(exception):
        db = g.pop("db", None)
        if db is not None:
            db.close()

    from .routes.main import main_bp
    app.register_blueprint(main_bp)  

    from .api.v1.adquisiciones import adquisiciones_bp   
    app.register_blueprint(adquisiciones_bp, url_prefix='/api/v1/adquisiciones')

    from .api.v1.historial import historial_bp
    app.register_blueprint(historial_bp, url_prefix='/api/v1/historial')


    return app


