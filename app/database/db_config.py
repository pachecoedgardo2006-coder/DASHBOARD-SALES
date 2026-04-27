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
            return cursor.fetchone() # Retorna una tupla (user, hash, rol) o None
        
    def get_resumen_dashboard(self):
        """Obtiene datos clave para las tarjetas del Dashboard."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            # Total ventas
            cursor.execute("SELECT SUM(total) FROM ventas")
            total_ventas = cursor.fetchone()[0] or 0
            
            # Cantidad de productos
            cursor.execute("SELECT COUNT(*) FROM productos")
            total_productos = cursor.fetchone()[0] or 0
            
            return total_ventas, total_productos
    
    def get_stats_resumen(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            # Sumamos el total de todas las ventas
            cursor.execute("SELECT SUM(total) FROM ventas")
            total_dinero = cursor.fetchone()[0] or 0.0
            
            # Contamos cuántos productos diferentes tenemos
            cursor.execute("SELECT COUNT(*) FROM productos")
            total_productos = cursor.fetchone()[0] or 0
            
            return total_dinero, total_productos