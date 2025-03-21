from app.db import db

class Proveedor(db.Model):
    __tablename__ = 'proveedores'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    proveedor = db.Column(db.String(100))
   