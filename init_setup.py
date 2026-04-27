from app.database.db_config import Database
from app.auth.password_hasher import PasswordHasher

def crear_admin_inicial():
    db = Database()
    hasher = PasswordHasher()
    
    # 1. Aseguramos que las tablas existan
    db.setup_database()
    
    # 2. Datos del admin (Cámbialos a tu gusto)
    username = "admin"
    password_plana = "Admin123" # Esta es la que escribirás en el login
    
    # 3. Hasheo de seguridad
    pw_hash = hasher.hash_password(password_plana)
    
    # 4. Insertar en la DB
    query = "INSERT INTO usuarios (username, password_hash, rol) VALUES (?, ?, ?)"
    
    try:
        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (username, pw_hash, "administrador"))
            conn.commit()
            print(f"✅ Usuario '{username}' creado exitosamente.")
            print(f"🔐 Hash generado: {pw_hash}")
    except Exception as e:
        if "UNIQUE constraint failed" in str(e):
            print("⚠️ El usuario ya existe en la base de datos.")
        else:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    crear_admin_inicial()