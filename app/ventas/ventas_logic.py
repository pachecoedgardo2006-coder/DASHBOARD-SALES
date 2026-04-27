from app.database.db_config import Database

class VentasLogic:
    def __init__(self):
        self.db = Database()

    def procesar_venta(self, producto_id, cantidad):
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            
            # 1. Verificar stock actual
            cursor.execute("SELECT stock, precio FROM productos WHERE id = ?", (producto_id,))
            producto = cursor.fetchone()
            
            if not producto or producto[0] < cantidad:
                return False, "Stock insuficiente o producto no existe"
            
            stock_actual, precio_unitario = producto
            total = precio_unitario * cantidad
            
            # 2. Descontar del inventario
            cursor.execute("UPDATE productos SET stock = stock - ? WHERE id = ?", (cantidad, producto_id))
            
            # 3. Registrar la venta
            cursor.execute("INSERT INTO ventas (producto_id, cantidad, total) VALUES (?, ?, ?)", 
                           (producto_id, cantidad, total))
            
            conn.commit()
            return True, f"Venta realizada por ${total}"