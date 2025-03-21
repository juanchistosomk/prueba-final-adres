from flask_sqlalchemy import SQLAlchemy
from flask import g, current_app
import sqlite3

#db = SQLAlchemy()

# Configuracion de la base de datos
def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(current_app.config['DATABASE'])
        g.db.row_factory = sqlite3.Row
    return g.db


def rows_to_dicts(rows):
    return [dict(row) for row in rows]