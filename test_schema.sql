PRAGMA encoding = "UTF-8";

CREATE TABLE IF NOT EXISTS proveedores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    proveedor TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS tipos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tipo TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS unidades (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    unidad TEXT NOT NULL
);


-- Poblar tablas con datos demo
INSERT INTO unidades (unidad) VALUES ('Dirección de Medicamentos y Tecnologías en Salud'),('Unidad 2'), ('Unidad 3');
INSERT INTO proveedores(proveedor) VALUES ('Laboratorios Bayer S.A.'),('TechSolutions SAS');
INSERT INTO tipos (tipo) VALUES ('Medicamentos'),('Tipo 2'),('Tipo 3');



CREATE TABLE IF NOT EXISTS adquisiciones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    presupuesto INTEGER NOT NULL, 
    id_unidad  INTEGER NOT NULL, 
    id_tipo INTEGER NOT NULL, 
    cantidad INTEGER NOT NULL, 
    valor_unitario INTEGER NOT NULL, 
    valor_total INTEGER NOT NULL, 
    fecha_adquisicion DATE NOT NULL, 
    id_proveedor INT NOT NULL,
    documentacion TEXT,
    estado TEXT NOT NULL CHECK (estado IN ('ACTIVO', 'INACTIVO')) DEFAULT 'ACTIVO',
    FOREIGN KEY (id_proveedor) REFERENCES proveedores(id),
    FOREIGN KEY (id_unidad) REFERENCES unidades(id),
    FOREIGN KEY (id_tipo) REFERENCES tipos(id)
);


