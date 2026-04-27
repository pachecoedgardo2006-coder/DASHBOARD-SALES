from app.auth.password_hasher import PasswordHasher
from app.database.db_config import Database

class AuthService:
    def __init__(self):
        self.hasher = PasswordHasher()
        self.db = Database()

    def login(self, username, typed_password):
        # 1. Buscar el usuario en la base de datos
        user_data = self.db.get_user_by_username(username)
        
        if user_data:
            # user_data[1] es el hash guardado en la DB
            stored_hash = user_data[1]
            if self.hasher.verify_password(typed_password, stored_hash):
                return True # Credenciales correctas
        
        return False # Usuario no existe o contraseña mal