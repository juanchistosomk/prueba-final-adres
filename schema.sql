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

INSERT INTO adquisiciones (presupuesto, id_unidad, id_tipo, cantidad, valor_unitario, valor_total, fecha_adquisicion, id_proveedor, documentacion) VALUES 
(1000000, 1, 1, 2, 10000, 20000, '2021-01-01', 1, 'O.C. No. 2021-07-20-001, fact No. 2023-07-20-001'),
(7000000, 1, 2, 1, 80000, 80000, '2025-01-01', 1, 'O.C. No. 2025-07-20-021, fact No. 2025-07-20-001'),
(2560000, 3, 3, 1, 50000, 50000, '2025-03-01', 1, 'O.C. No. 2025-07-20-040, fact No. 2025-07-20-001'),
(8990000, 2, 2, 1, 30000, 30000, '2024-11-21', 2, 'O.C. No. 2024-07-20-034, fact No. 2025-07-20-001'),
(3120000, 3, 1, 1, 89000, 89000, '2025-02-09', 2, 'O.C. No. 2025-07-20-088, fact No. 2025-07-20-001'),
(4100000, 2, 3, 1, 15000, 15000, '2025-03-19', 2, 'O.C. No. 2025-07-20-099, fact No. 2025-07-20-001');


CREATE TABLE IF NOT EXISTS historial_adquisicion (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fecha_modificacion TIMESTAMP NOT NULL,
    tipo_modificacion TEXT NOT NULL,
    id_adquisicion INTEGER NOT NULL,
    presupuesto INTEGER NOT NULL, 
    id_unidad  INTEGER NOT NULL, 
    id_tipo INTEGER NOT NULL, 
    cantidad INTEGER NOT NULL, 
    valor_unitario REAL NOT NULL, 
    valor_total INTEGER NOT NULL, 
    fecha_adquisicion DATE NOT NULL, 
    id_proveedor INTEGER NOT NULL,
    documentacion TEXT,
    estado TEXT NOT NULL CHECK (estado IN ('ACTIVO', 'INACTIVO')) DEFAULT 'ACTIVO',
    usuario_modificacion TEXT NOT NULL DEFAULT 'admin@adres.gov.co'
);



-- Relaciones para otros motores como Mysql

--ALTER TABLE adquisiciones ADD CONSTRAINT fk_proveedor FOREIGN KEY (id_proveedor) REFERENCES proveedores(id);
--ALTER TABLE adquisiciones ADD CONSTRAINT fk_unidad FOREIGN KEY (id_unidad) REFERENCES unidad(id);
--ALTER TABLE adquisiciones ADD CONSTRAINT fk_tipo FOREIGN KEY (id_tipo) REFERENCES tipo(id);



---------------TRIGGERs para HISTORIAL----------------

CREATE TRIGGER IF NOT EXISTS historial_adquisicion_insert
AFTER INSERT ON adquisiciones
BEGIN
    INSERT INTO historial_adquisicion (fecha_modificacion, tipo_modificacion, id_adquisicion, presupuesto, id_unidad, id_tipo, cantidad, valor_unitario, valor_total, fecha_adquisicion, id_proveedor, documentacion, estado)
    VALUES (DATETIME(CURRENT_TIMESTAMP, '-5 hours'), 'INSERTADO', NEW.id, NEW.presupuesto, NEW.id_unidad, NEW.id_tipo, NEW.cantidad, NEW.valor_unitario, NEW.valor_total, NEW.fecha_adquisicion, NEW.id_proveedor, NEW.documentacion, NEW.estado);
END;


CREATE TRIGGER IF NOT EXISTS historial_adquisicion_update
AFTER UPDATE ON adquisiciones
BEGIN
    INSERT INTO historial_adquisicion (fecha_modificacion, tipo_modificacion, id_adquisicion, presupuesto, id_unidad, id_tipo, cantidad, valor_unitario, valor_total, fecha_adquisicion, id_proveedor, documentacion, estado)
    VALUES (DATETIME(CURRENT_TIMESTAMP, '-5 hours'), 'MODIFICADO', NEW.id, NEW.presupuesto, NEW.id_unidad, NEW.id_tipo, NEW.cantidad, NEW.valor_unitario, NEW.valor_total, NEW.fecha_adquisicion, NEW.id_proveedor, NEW.documentacion, NEW.estado);
    
END;