from app.database.db_config import Database
from datetime import datetime

class VentasLogic:
    def __init__(self):
        self.db = Database()

    def procesar_venta(self, producto_id, cantidad):
        """Procesa una transacción con validación de integridad y retorna el estado."""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            
            # Validar existencia y stock
            cursor.execute("SELECT nombre, stock, precio FROM productos WHERE id = ?", (producto_id,))
            producto = cursor.fetchone()
            
            if not producto:
                return False, "Producto no encontrado"
            
            nombre, stock_actual, precio_unitario = producto
            
            if stock_actual < cantidad:
                return False, f"Stock insuficiente para {nombre} (Disponible: {stock_actual})"
            
            total = precio_unitario * cantidad
            
            try:
                # Actualización de inventario y registro de venta en una sola transacción
                cursor.execute("UPDATE productos SET stock = stock - ? WHERE id = ?", (cantidad, producto_id))
                
                cursor.execute(
                    "INSERT INTO ventas (producto_id, cantidad, total, fecha_venta) VALUES (?, ?, ?, ?)", 
                    (producto_id, cantidad, total, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                )
                
                conn.commit()
                return True, f"Venta exitosa: {cantidad}x {nombre} - Total: ${total:,.2f}"
            except Exception as e:
                conn.rollback()
                return False, f"Error en la base de datos: {str(e)}"

    def obtener_kpis_ventas(self):
        """Calcula indicadores clave para los widgets del dashboard."""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            
            # Total ventas hoy
            cursor.execute("SELECT SUM(total) FROM ventas WHERE date(fecha_venta) = date('now')")
            hoy = cursor.fetchone()[0] or 0
            
            # Ticket promedio
            cursor.execute("SELECT AVG(total) FROM ventas")
            promedio = cursor.fetchone()[0] or 0
            
            # Producto más vendido (Top 1)
            cursor.execute("""
                SELECT p.nombre, SUM(v.cantidad) as total_vendido 
                FROM ventas v 
                JOIN productos p ON v.producto_id = p.id 
                GROUP BY v.producto_id 
                ORDER BY total_vendido DESC LIMIT 1
            """)
            top = cursor.fetchone()
            top_nombre = top[0] if top else "N/A"
            
            return {
                "ventas_hoy": f"${hoy:,.2f}",
                "ticket_promedio": f"${promedio:,.2f}",
                "producto_top": top_nombre
            }

    def obtener_historial_reciente(self, limite=10):
        """Retorna las últimas ventas con nombres de productos."""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT v.id, p.nombre, v.cantidad, v.total, v.fecha_venta 
                FROM ventas v
                JOIN productos p ON v.producto_id = p.id
                ORDER BY v.fecha_venta DESC LIMIT ?
            """, (limite,))
            return cursor.fetchall()