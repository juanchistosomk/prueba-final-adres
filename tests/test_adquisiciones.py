import pytest
import os
from app import create_app, get_db
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning, module="flask_restx")

##################### TESTING DE ADQUISICIONES #####################


@pytest.fixture(scope="session", autouse=True)
def cleanup_db():
    """Limpia la base de datos de prueba antes de la sesión de pruebas."""
    db_path = schema_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),'../test.db')
    if os.path.exists(db_path):
        os.remove(db_path)
    yield 



@pytest.fixture(scope="session")
def app():
    # Configurar la aplicación Flask para pruebas
    app = create_app()
    app.config['TESTING'] = True
    app.config['DATABASE'] = 'test.db'  #':memory:' 
    with app.app_context():
        init_test_db()
    yield app

@pytest.fixture
def client(app):
    # Cliente de prueba
    return app.test_client()



def init_test_db():   
    db = get_db()
    schema_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),'../test_schema.sql')
    try:
        
        with open(schema_path, mode='r', encoding='utf-8') as f:
            db.cursor().executescript(f.read())
       
        # Insertar datos iniciales
        db.cursor().executescript("""
            INSERT INTO adquisiciones (presupuesto, id_unidad, id_tipo, cantidad, valor_unitario, valor_total, fecha_adquisicion, id_proveedor, documentacion, estado)
            VALUES (10000, 1, 1, 10, 100, 1000, '2025-03-20', 1, 'documento test', 'ACTIVO');
        
            INSERT INTO adquisiciones (presupuesto, id_unidad, id_tipo, cantidad, valor_unitario, valor_total, fecha_adquisicion, id_proveedor, documentacion, estado)
            VALUES (20000, 2, 1, 20, 200, 4000, '2025-03-21', 2, 'Otro documento test', 'ACTIVO');
        """)
        db.commit()
    except Exception as e:
        print(f"Error al ejecutar el esquema SQL: {e}")
        raise 


def test_list(client):
    '''
    Prueba para listar todas las adquisiciones activas
    '''
    response = client.get('/api/v1/adquisiciones/list')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert data[0]['estado'] == 'ACTIVO'


def test_list_one(client):
    '''
    Prueba para filtrar una adquisición
    '''
    payload = {'presupuesto': 20000}
    response = client.post('/api/v1/adquisiciones/list-one', data=payload)
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]['presupuesto'] == 20000


def test_desactive(client):
    '''
    Prueba para desactivar una adquisición
    '''
    adquisicion_id = 1
    response = client.get(f'/api/v1/adquisiciones/desactive/{adquisicion_id}')
    assert response.status_code == 200
    data = response.get_json()
    assert data['message'] == '✅Adquisición desactivada exitosamente.'

    # Verificación
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT estado FROM adquisiciones WHERE id = ?", (adquisicion_id,))
    estado = cursor.fetchone()['estado']
    assert estado == 'INACTIVO'


def test_create(client):
    '''
    Prueba para crear una nueva adquisición
    '''
    payload = {
        'presupuesto': 30000,
        'unidad': 3,
        'tipo': 2,
        'cantidad': 15,
        'valorUnitario': 2000,
        'valorTotal': 30000,
        'fechaAdquisicion': '2025-03-22',
        'proveedor': 3,
        'documentacion': 'Orden de compra No. 2023-07-20-001, factura No. 2023-07-20-001'
    }
    response = client.post('/api/v1/adquisiciones/create', data=payload)
    assert response.status_code == 201
    #data = response.get_json()
    #assert data['message'] == '✅Adquisición creada exitosamente.'
    html_content = response.data.decode('utf-8')  # Obtener HTML
    assert '✅Adquisición creada exitosamente.' in html_content  

    # Verificar 
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM adquisiciones WHERE presupuesto = ?", (payload['presupuesto'],))
    nueva_adquisicion = cursor.fetchone()
    assert nueva_adquisicion is not None
    assert nueva_adquisicion['estado'] == 'ACTIVO'


def test_edit_adquisicion(client):
    '''
    Prueba para editar una adquisición
    '''
    payload = {
        'idAdquisicion': 2,
        'presupuesto': 25000,
        'unidad': 2,
        'tipo': 2,
        'cantidad': 20,
        'valorUnitario': 1250,
        'valorTotal': 25000,
        'fechaAdquisicion': '2025-03-23',
        'proveedor': 1,
        'documentacion': 'Adquisición Editada'        
    }
    response = client.post('/api/v1/adquisiciones/edit', data=payload)
    assert response.status_code == 200   
    html_content = response.data.decode('utf-8')  # Obtener HTML
    assert '✅Adquisición actualizada exitosamente.' in html_content  

    # Verificar 
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM adquisiciones WHERE id = ?", (payload['idAdquisicion'],))
    adquisicion_editada = cursor.fetchone()
    assert adquisicion_editada['presupuesto'] == payload['presupuesto']
    assert adquisicion_editada['documentacion'] == payload['documentacion']
