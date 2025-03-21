from app.db import db

class Adquisicion(db.Model):
    __tablename__ = 'adquisiciones'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    presupuesto = db.Column(db.String(100), nullable=False)
    id_unidad = db.Column(db.Integer, db.ForeignKey('unidades.id'))
    id_tipo = db.Column(db.Integer, db.ForeignKey('tipos.id'))
    cantidad = db.Column(db.Integer, nullable=False)
    valor_unitario = db.Column(db.Integer, nullable=False)
    valor_total = db.Column(db.Integer, nullable=False)
    fecha_adquisicion = db.Column(db.String(100), nullable=False)
    id_proveedor = db.Column(db.Integer, db.ForeignKey('proveedores.id'))
    documentacion = db.Column(db.String(100))
    estado = db.Column(db.String(100))

 
    unidad = db.relationship('Unidad', backref='adquisiciones', lazy=True)
    proveedor = db.relationship('Proveedor', backref='adquisiciones', lazy=True)
    tipo = db.relationship('Tipo', backref='adquisiciones', lazy=True)


    def save(self):
        db.session.add(self)
        db.session.commit()


