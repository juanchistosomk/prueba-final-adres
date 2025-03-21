from app.db import db

class Tipo(db.Model):
    __tablename__ = 'tipos'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tipo = db.Column(db.String(100))
    