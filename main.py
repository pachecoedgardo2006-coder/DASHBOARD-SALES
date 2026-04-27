from app.database.db_config import Database
from app.ui.views.login_view import LoginView

def main():
    # Inicializar DB en segundo plano
    db = Database()
    db.setup_database()

    # Lanzar Interfaz
    app = LoginView()
    app.mainloop()

if __name__ == "__main__":
    main()