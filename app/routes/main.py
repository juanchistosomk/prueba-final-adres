from flask import render_template, Blueprint, current_app, jsonify
import sqlite3
main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    try:
        current_app.logger.info("Main route")
        db = sqlite3.connect(current_app.config['DATABASE'])
        cursor = db.cursor()
    
        # Carga selects    
        proveedores = cursor.execute('SELECT id, proveedor FROM proveedores').fetchall()
        tipos = cursor.execute('SELECT id, tipo FROM tipos').fetchall()
        unidades = cursor.execute('SELECT id, unidad FROM unidades').fetchall()
        return render_template('index.html', proveedores=proveedores, unidades=unidades, tipos=tipos), 200
    except Exception as e:
        current_app.logger.error(f"🔴 Error al cargar index: {e}")
        return render_template('index.html', proveedores=[], unidades=[], tipos=[]), 500




@main_bp.route('/crear-adquisicion')
def crear_adquisicion():
    try:
        current_app.logger.info("Main route")
        db = sqlite3.connect(current_app.config['DATABASE'])
        cursor = db.cursor()
    
        # Carga selects    
        proveedores = cursor.execute('SELECT id, proveedor FROM proveedores').fetchall()
        tipos = cursor.execute('SELECT id, tipo FROM tipos').fetchall()
        unidades = cursor.execute('SELECT id, unidad FROM unidades').fetchall()
        db.commit()
        db.close()
        return render_template('crear-adquisicion.html', proveedores=proveedores, unidades=unidades, tipos=tipos, selected_proveedor='', selected_unidad='', selected_tipo=''), 200
     
    except Exception as e:
        current_app.logger.error(f"🔴 Error al cargar inicio: {e}")
        return render_template('crear-adquisicion.html', proveedores=[], unidades=[], tipos=[], selected_proveedor='', selected_unidad='', selected_tipo=''), 500




@main_bp.route('/editar-adquisicion/<int:adquisicion_id>', methods=['GET'])
def editar_adquisicion(adquisicion_id):
    try:
        db = sqlite3.connect(current_app.config['DATABASE'])
        cursor = db.cursor()
        cursor.execute('SELECT * FROM adquisiciones WHERE id = ?', (adquisicion_id,))
        adquisicion = cursor.fetchone() 

        # Carga selects    
        proveedores = cursor.execute('SELECT id, proveedor FROM proveedores').fetchall()
        tipos = cursor.execute('SELECT id, tipo FROM tipos').fetchall()
        unidades = cursor.execute('SELECT id, unidad FROM unidades').fetchall()
        db.close()
        
        return render_template('editar-adquisicion.html', adquisicion=adquisicion, proveedores=proveedores, unidades=unidades, tipos=tipos)
    except Exception as e:
        current_app.logger.error(f"🔴 Error al obtener adquisición: {e}")
        return render_template('editar-adquisicion.html', adquisicion=None, proveedores=[], unidades=[], tipos=[])



@main_bp.route('/historial')
def historial_adquisicion():
    return render_template('historial.html')

