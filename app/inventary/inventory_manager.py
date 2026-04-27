from app.database.db_config import Database

class InventoryManager:
    def __init__(self):
        self.db = Database()

    def agregar_producto(self, nombre, precio, stock, categoria):
        if precio <= 0 or stock < 0:
            return False, "Precio o stock inválidos"
        
        query = "INSERT INTO productos (nombre, precio, stock, categoria) VALUES (?, ?, ?, ?)"
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (nombre, precio, stock, categoria))
            conn.commit()
            return True, "Producto agregado"

    def consultar_stock_bajo(self, limite=5):
        """Alerta de ciberseguridad/operaciones: detectar faltantes."""
        query = "SELECT nombre, stock FROM productos WHERE stock <= ?"
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (limite,))
            return cursor.fetchall()