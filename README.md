# 📝Prueba Técnica Final: Gestión de Adquisiciones ADRES

## Por: Ing. JUAN CARLOS CASTILLO G.

<a href="https://freeimage.host/i/3z3afwJ" target="_blank"><img src="https://iili.io/3z3afwJ.md.png" border="0"></a>
<a href="https://freeimage.host/i/3zqda3l" target="_blank"><img src="https://iili.io/3zqda3l.md.png" border="0"></a>
<a href="https://freeimage.host/i/3zfJh8P" target="_blank"><img src="https://iili.io/3zfJh8P.md.png" border="0"></a>

### Descripción

Este proyecto esta basado en una aplicación web desarrollada con Flask MVC que permite gestionar el registro de requerimientos de adquisiciones de la ADRES, ya sean bienes o servicios. Los registros se almacenan en una base de datos SQLite, diseño resposive, campos en formularios validados, avisos en acción de creación modificación y desactivación, variables de entorno, Testing, versionamiento de API, creación automática de base de datos con tablas y datos dummy, manejo de errores, y la aplicación incluye los siguientes endpoints:

- /create : crea un nuevo registro de adquisición.
- /edit : permite editar información de una adquisición.
- /desactivate : inactiva regitros de adquisiciones.
- /list : listar información de las adquisiciones existentes.
- /list-one : lista información de adquisiciones especificas en base a filtros.
- /historial/list : lista los registros del historial de cambios de las adquisiciones.

### Características

- Creación de registros.
- Búsqueda de registros con diferentes filtros.
- Revisión del historial de cambios.
- Desactivación de registros específicos de adquisiciones.
- Modificación de registros de adquisiciones.

## Tecnologias implementadas: HTML, CSS, JavaScript, Bootstrap, Python Flask, SQLite, GitHub

## Requisitos

- Python 3.9 o superior.
- Flask.
- SQLite3.
- Flask_sqlalchemy

## Instalación

1. Clona el repositorio:

   ```bash
   git clone https://github.com/juanchistosomk/prueba-final-adres.git
   cd prueba_tecnica_final
   ```

### 2. Comandos crear entorno virtual python:

```bash
python -m venv env
```

```bash
.\env\Scripts\activate
```

### 3. Instalar dependencias:

```bash
pip install -r requirements.txt
```

### 4. Ejecutar el proyecto:

```bash
python run.py
```

### 5. Abrir URL:

http://localhost:5000

### 6. Ejecutar Tests de calidad:

```bash
pytest -v tests/test_adquisiciones.py
```
