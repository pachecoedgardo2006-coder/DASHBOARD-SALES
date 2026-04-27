import sqlite3
from app.database.models import CREATE_USERS_TABLE, CREATE_INVENTARIO_TABLE, CREATE_VENTAS_TABLE

class Database:
    def __init__(self, db_name="database.db"):
        self.db_name = db_name

    def get_connection(self):
        """Crea una conexión y activa las llaves foráneas."""
        conn = sqlite3.connect(self.db_name)
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn

    def setup_database(self):
        """Crea las tablas iniciales si no existen."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(CREATE_USERS_TABLE)
            cursor.execute(CREATE_INVENTARIO_TABLE)
            cursor.execute(CREATE_VENTAS_TABLE)
            conn.commit()
            print("Base de datos inicializada con éxito.")

    def get_user_by_username(self, username):
        """Busca un usuario en la base de datos y retorna sus datos."""
        query = "SELECT username, password_hash, rol FROM usuarios WHERE username = ?"
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (username,))
            return cursor.fetchone() 
        
    def get_resumen_dashboard(self):
        """Mantiene tu lógica original para los totales."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT SUM(total) FROM ventas")
            total_ventas = cursor.fetchone()[0] or 0
            
            cursor.execute("SELECT COUNT(*) FROM productos")
            total_productos = cursor.fetchone()[0] or 0
            
            return total_ventas, total_productos

    # --- NUEVOS MÉTODOS PARA EL DASHBOARD MEJORADO ---

    def get_alertas_stock(self):
        """Consulta corregida para obtener productos con stock bajo."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM productos WHERE stock < 5")
            return cursor.fetchone()[0] or 0

    def get_ultimas_ventas(self, limite=5):
        """Obtiene el historial para el monitor de actividad."""
        query = """
            SELECT v.fecha_venta, p.nombre, v.total 
            FROM ventas v 
            JOIN productos p ON v.producto_id = p.id 
            ORDER BY v.fecha_venta DESC LIMIT ?
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (limite,))
            return cursor.fetchall()