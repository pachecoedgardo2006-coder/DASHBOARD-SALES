import customtkinter as ctk
from tkinter import messagebox
from app.auth.auth_service import AuthService
from app.ui.views.dashboard_view import DashboardView

class LoginView(ctk.CTk):
    def __init__(self):
        super().__init__()

        
        self.auth_service = AuthService()
        self.title("Dark Mystic Dashboard - Login")
        self.geometry("400x550")
        self.configure(fg_color="#0a0a0a")  # Fondo casi negro profundo

        # Contenedor Central (El "Glass" Card)
        self.glass_frame = ctk.CTkFrame(
            self, 
            corner_radius=20, 
            fg_color="#1a1a1a", # Gris muy oscuro
            border_width=1,
            border_color="#3d0066" # Borde morado sutil
        )
        self.glass_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.8, relheight=0.7)

        # Título
        self.label = ctk.CTkLabel(
            self.glass_frame, 
            text="BIENVENIDO", 
            font=("Orbitron", 24, "bold"), 
            text_color="#a855f7" # Morado brillante
        )
        self.label.pack(pady=(40, 20))

        # Inputs
        self.user_input = ctk.CTkEntry(
            self.glass_frame, 
            placeholder_text="Usuario", 
            height=45, 
            fg_color="#0f0f0f",
            border_color="#3d0066"
        )
        self.user_input.pack(pady=10, padx=30, fill="x")

        self.pass_input = ctk.CTkEntry(
            self.glass_frame, 
            placeholder_text="Contraseña", 
            show="*", 
            height=45, 
            fg_color="#0f0f0f",
            border_color="#3d0066"
        )
        self.pass_input.pack(pady=10, padx=30, fill="x")

        # Botón de Entrada
        self.login_button = ctk.CTkButton(
            self.glass_frame, 
            text="ACCEDER", 
            fg_color="#6b21a8", 
            hover_color="#7e22ce",
            height=45,
            font=("Segoe UI", 14, "bold")
        )
        self.login_button.pack(pady=(30, 10), padx=30, fill="x")

        self.login_button.configure(command=self.ejecutar_login)

    def ejecutar_login(self):
            user = self.user_input.get()
            password = self.pass_input.get()

            if not user or not password:
                messagebox.showwarning("Atención", "Por favor rellena todos los campos")
                return

            # Ahora el servicio se encarga de todo (DB + Hashing)
            if self.auth_service.login(user, password):
                print("Acceso exitoso")
                self.withdraw()
                # abrimos el dash

                self.abrir_dashboard()

            else:
                messagebox.showerror("Error", "Usuario o contraseña incorrectos")

    def abrir_dashboard(self):
        self.dash_window = DashboardView() # Creamos la instancia del Dashboard
        self.dash_window.protocol("WM_DELETE_WINDOW", self.cerrar_todo) # Si cierra dash, cierra todo
        self.dash_window.mainloop()


    def cerrar_todo(self):
        self.dash_window.destroy()
        self.destroy()

if __name__ == "__main__":
    app = LoginView()
    app.mainloop()