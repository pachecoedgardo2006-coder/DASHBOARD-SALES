import bcrypt

class PasswordHasher:
    @staticmethod
    def hash_password(password: str) -> str:
        """Transforma la contraseña plana en un hash seguro."""
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

    @staticmethod
    def verify_password(password: str, hashed_password: str) -> bool:
        """Compara la contraseña ingresada con el hash guardado."""
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))