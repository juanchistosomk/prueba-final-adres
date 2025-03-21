from flask import render_template, request, redirect, current_app, jsonify
from app.db import get_db, rows_to_dicts
from . import historial_bp



@historial_bp.route('/list', methods=['GET'])
def historial_adquisicion():
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute('''SELECT ha.id, ha.fecha_modificacion, ha.tipo_modificacion, ha.usuario_modificacion, ha.presupuesto, ha.cantidad, ha.valor_unitario, ha.valor_total, ha.fecha_adquisicion, p.proveedor, t.tipo, u.unidad, ha.id_adquisicion, ha.id_proveedor, ha.id_tipo, ha.estado
                       FROM historial_adquisicion ha
                       INNER JOIN adquisiciones a ON ha.id_adquisicion = a.id
                       INNER JOIN proveedores p ON a.id_proveedor = p.id
                       INNER JOIN tipos t ON a.id_tipo = t.id
                       INNER JOIN unidades u ON a.id_unidad = u.id                       
                       ORDER BY ha.id_adquisicion DESC, ha.fecha_modificacion DESC''')
        historial_adquisiciones = rows_to_dicts(cursor.fetchall())
        return jsonify(historial_adquisiciones), 200
    except Exception as e:
        current_app.logger.error(f"🔴 Error al obtener historial: {e}")
        return jsonify([])