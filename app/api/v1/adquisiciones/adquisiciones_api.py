from flask import request, jsonify, render_template, request, current_app, redirect, url_for
from datetime import datetime
import os, re
from app.db import get_db, rows_to_dicts
from . import adquisiciones_bp

HOY = datetime.today().strftime('%Y-%m-%d')

   
    

@adquisiciones_bp.route('/list', methods=['GET'])
def lista_adquisiciones():
    '''
    Listado de adquisiciones
    '''
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute('''SELECT a.presupuesto, u.unidad, t.tipo, a.cantidad, a.valor_unitario, a.valor_total, a.fecha_adquisicion, p.proveedor, a.documentacion, a.estado
                       FROM adquisiciones a
                       INNER JOIN proveedores p ON a.id_proveedor = p.id
                       INNER JOIN tipos t ON a.id_tipo = t.id
                       INNER JOIN unidades u ON a.id_unidad = u.id
                       WHERE a.estado = 'ACTIVO'
                       ORDER BY a.id DESC
                       ''')
        adquisiciones = rows_to_dicts(cursor.fetchall())        
        #db.close()

        return jsonify(adquisiciones), 200
    
    except Exception as e:
        current_app.logger.error(f"Error al listar las adquisiciones_: {e}")
        return jsonify([]), 500
    



@adquisiciones_bp.route('/list-one', methods=['POST'])
def buscar_adquisiciones():
    '''
    Búsqueda de adquisiciones
    '''
    try:

        presupuesto = request.form.get('presupuesto')
        unidad= request.form.get('unidad')
        tipo= request.form.get('tipo')
        cantidad= request.form.get('cantidad')
        valor_unitario= request.form.get('valorUnitario')
        valor_total= request.form.get('valorTotal')
        fecha_adquisicion= request.form.get('fechaAdquisicion')
        proveedor= request.form.get('proveedor')
        documentacion= request.form.get('documentacion')

        add_filter = ""
        if presupuesto:
            add_filter += f" AND a.presupuesto LIKE '%{presupuesto}%'"
        if unidad:
            add_filter += f" AND a.id_unidad = '{unidad}'"
        if tipo:
            add_filter += f" AND a.id_tipo = '{tipo}'"
        if cantidad:
            add_filter += f" AND a.cantidad = '{cantidad}'"
        if valor_unitario:
            add_filter += f" AND a.valor_unitario = '{valor_unitario}'"
        if valor_total:
            add_filter += f" AND a.valor_total = '{valor_total}'"
        if fecha_adquisicion:
            add_filter += f" AND a.fecha_adquisicion = '{fecha_adquisicion}'"
        if proveedor:
            add_filter += f" AND a.id_proveedor = '{proveedor}'"
        if documentacion:
            add_filter += f" AND a.documentacion LIKE '%{documentacion}%'"

     

        db = get_db()
        cursor = db.cursor()
        cursor.execute('''SELECT a.id, a.presupuesto, u.unidad, t.tipo, a.cantidad, a.valor_unitario, a.valor_total, a.fecha_adquisicion, p.proveedor, a.documentacion, a.estado
                       FROM adquisiciones a
                       INNER JOIN proveedores p ON a.id_proveedor = p.id
                       INNER JOIN tipos t ON a.id_tipo = t.id
                       INNER JOIN unidades u ON a.id_unidad = u.id
                       WHERE 1 = 1 AND a.estado = 'ACTIVO' 
                       ''' + add_filter + " ORDER BY a.id DESC")
        adquisiciones = rows_to_dicts(cursor.fetchall())    
       
        return jsonify(adquisiciones), 200
    
    except Exception as e:
        current_app.logger.error(f"Error al listar las adquisiciones: {e}")
        return jsonify([])




@adquisiciones_bp.route('/create', methods=['POST'])
def crear_adquisicion():
    '''
    Crear adquisiciones
    '''
    try:
            
        db = get_db()
        cursor = db.cursor()

         # Verificar si la tabla 'adquisiciones' existe
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='adquisiciones'")
        table_exists = cursor.fetchone()
        if not table_exists:
            current_app.logger.info("🔴 La tabla 'adquisiciones' no existe. Se esta creando automáticamente...")
            with current_app.open_resource('../schema.sql', mode='r') as f:
                db.cursor().executescript(f.read())
            db.commit()
                  
        presupuesto = request.form.get('presupuesto')
        unidad= request.form.get('unidad')
        tipo= request.form.get('tipo')
        cantidad= request.form.get('cantidad')
        valor_unitario= request.form.get('valorUnitario')
        valor_total= request.form.get('valorTotal')
        fecha_adquisicion= request.form.get('fechaAdquisicion')
        proveedor= request.form.get('proveedor')
        documentacion= request.form.get('documentacion')

  
        proveedores = cursor.execute('SELECT id, proveedor FROM proveedores').fetchall()
        tipos = cursor.execute('SELECT id, tipo FROM tipos').fetchall()
        unidades = cursor.execute('SELECT id, unidad FROM unidades').fetchall()  
            
        # Insertar adquisiciones
        cursor.execute('''
                INSERT INTO adquisiciones (presupuesto, id_unidad, id_tipo, cantidad, valor_unitario, valor_total, fecha_adquisicion, id_proveedor, documentacion)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (presupuesto, unidad, tipo, cantidad, valor_unitario, valor_total, fecha_adquisicion, proveedor, documentacion))
        db.commit()
        #db.close()
        message = {"message": "✅Adquisición creada exitosamente.", "status": 200}
        return render_template('crear-adquisicion.html', message=message, request=request, proveedores=proveedores, unidades=unidades, tipos=tipos, selected_proveedor=int(proveedor), selected_unidad=int(unidad), selected_tipo=int(tipo)), 201
    except Exception as e:
        current_app.logger.error(f"🔴 Error al capturar adquisiciones: {e}")
        message = {"message": "🔴Error al crear la adquisición, intente nuevamente.", "status": 500}
        return render_template('crear-adquisicion.html', message=message, request=request, proveedores=[], unidades=[], tipos=[], selected_proveedor=int(proveedor), selected_unidad=int(unidad), selected_tipo=int(tipo)), 500





@adquisiciones_bp.route('/edit', methods=['POST'])
def editar_adquisicion():
    '''
    Editar adquisiciones
    '''
    try:
        db = get_db()
        cursor = db.cursor()
        id = request.form.get('idAdquisicion')
        presupuesto = request.form.get('presupuesto')
        unidad= request.form.get('unidad')
        tipo= request.form.get('tipo')
        cantidad= request.form.get('cantidad')
        valor_unitario= request.form.get('valorUnitario')
        valor_total= request.form.get('valorTotal')
        fecha_adquisicion= request.form.get('fechaAdquisicion')
        proveedor= request.form.get('proveedor')
        documentacion= request.form.get('documentacion')

        

        # Carga selects    
        proveedores = cursor.execute('SELECT id, proveedor FROM proveedores').fetchall()
        tipos = cursor.execute('SELECT id, tipo FROM tipos').fetchall()
        unidades = cursor.execute('SELECT id, unidad FROM unidades').fetchall()

            
        cursor.execute('''
                UPDATE adquisiciones SET presupuesto=?, id_unidad=?, id_tipo=?, cantidad=?, valor_unitario=?, valor_total=?, fecha_adquisicion=?, id_proveedor=?, documentacion=? WHERE id=?
        ''', (presupuesto, unidad, tipo, cantidad, valor_unitario, valor_total, fecha_adquisicion, proveedor, documentacion, id))
        db.commit()
        
        adquisicion = cursor.execute('SELECT * FROM adquisiciones WHERE id = ?', (id,)).fetchone()

        message = {"message": "✅Adquisición actualizada exitosamente.", "status": 200}
        return render_template('editar-adquisicion.html', message=message, request=request, adquisicion=adquisicion, proveedores=proveedores,tipos=tipos, unidades=unidades), 200
    except Exception as e:
        current_app.logger.error(f"🔴 Error al capturar adquisiciones: {e}")
        message = {"message": "🔴Error al actualizar la adquisición, intente nuevamente.", "status": 500}
        return render_template('editar-adquisicion.html', message=message, request=request, adquisicion=[], proveedores=proveedores,tipos=tipos, unidades=unidades), 500
    

@adquisiciones_bp.route('/desactive/<int:adquisicion_id>', methods=['GET'])
def desactive_adquisiciones(adquisicion_id):
    '''
    Desactivar adquisiciones
    '''
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute('UPDATE adquisiciones SET estado = "INACTIVO" WHERE id = ?', (adquisicion_id,))
        db.commit()    

        return {"message": "✅Adquisición desactivada exitosamente.", "status": 200}, 200
    except Exception as e:
        current_app.logger.error(f"🔴 Error al desactivar adquisición: {e}")
        return {"message": "🔴Error al desactivar la adquisición, intente nuevamente.", "status": 500}, 500