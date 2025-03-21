from app.api import db

class Unidad(db.Model):
    __tablename__ = 'unidades'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    unidad = db.Column(db.String(100))