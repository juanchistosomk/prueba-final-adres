from app.db import db

class Historial(db.Model):
    __tablename__ = 'historial'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    usuario_modificacion = db.Column(db.String(100), nullable=False, default='admin@adres.gov.co')
    tipo_modificacion = db.Column(db.String(100), nullable=False)
    fecha_modificacion = db.Column(db.String(30), nullable=False)
    id_adquisicion = db.Column(db.Integer, db.ForeignKey('adquisiciones.id'))
    presupuesto = db.Column(db.Integer, nullable=False)
    id_proveedor = db.Column(db.Integer, db.ForeignKey('proveedores.id'))
    id_tipo = db.Column(db.Integer, db.ForeignKey('tipos.id'))
    id_unidad = db.Column(db.Integer, db.ForeignKey('unidades.id'))
    cantidad = db.Column(db.Integer, nullable=False)
    valor_unitario = db.Column(db.Integer, nullable=False)
    valor_total = db.Column(db.Integer, nullable=False)
    fecha_adquisicion = db.Column(db.Date, nullable=False)
    documentacion = db.Column(db.String(100))
    estado = db.Column(db.String(100))
