# Definimos las sentencias SQL para crear las tablas con integridad referencial y tipos de datos optimizados

CREATE_USERS_TABLE = """
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    rol TEXT DEFAULT 'vendedor',
    fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP
);
"""

CREATE_INVENTARIO_TABLE = """
CREATE TABLE IF NOT EXISTS productos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    precio REAL NOT NULL,
    stock INTEGER NOT NULL CHECK(stock >= 0),
    categoria TEXT,
    ultima_actualizacion DATETIME DEFAULT CURRENT_TIMESTAMP
);
"""

CREATE_VENTAS_TABLE = """
CREATE TABLE IF NOT EXISTS ventas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    producto_id INTEGER NOT NULL,
    cantidad INTEGER NOT NULL CHECK(cantidad > 0),
    total REAL NOT NULL,
    fecha_venta DATETIME DEFAULT CURRENT_TIMESTAMP,
    metodo_pago TEXT DEFAULT 'Efectivo',
    FOREIGN KEY (producto_id) REFERENCES productos (id) ON DELETE CASCADE
);
"""

# Índices para optimizar la velocidad de carga de los KPIs y el historial
CREATE_INDEX_VENTAS_FECHA = "CREATE INDEX IF NOT EXISTS idx_ventas_fecha ON ventas(fecha_venta);"
CREATE_INDEX_PRODUCTOS_NOMBRE = "CREATE INDEX IF NOT EXISTS idx_productos_nombre ON productos(nombre);"