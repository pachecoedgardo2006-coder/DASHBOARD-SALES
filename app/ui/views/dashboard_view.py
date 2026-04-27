import customtkinter as ctk
from app.database.db_config import Database
from app.ventas.ventas_logic import VentasLogic
from app.ui.views.resumen_view import ResumenView
from app.ui.views.inventario_view import InventarioView
from app.ui.views.ventas_view import VentasView

class DashboardView(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.db = Database()
        self.ventas_motor = VentasLogic()
        self.title("Dark Mystic - Sales System")
        self.geometry("1100x600")
        self.configure(fg_color="#0a0a0a")

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # SIDEBAR
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0, fg_color="#121212")
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        ctk.CTkLabel(self.sidebar, text="DASHBOARD", font=("Orbitron", 20, "bold"), text_color="#a855f7").pack(pady=30, padx=20)

        # Botones con navegación modular
        ctk.CTkButton(self.sidebar, text="🏠  Resumen", anchor="w", fg_color="transparent", 
                      command=self.mostrar_resumen).pack(fill="x", padx=10, pady=5)
        ctk.CTkButton(self.sidebar, text="💰  Ventas", anchor="w", fg_color="transparent", 
                      command=self.mostrar_ventas).pack(fill="x", padx=10, pady=5)
        ctk.CTkButton(self.sidebar, text="📦  Inventario", anchor="w", fg_color="transparent", 
                      command=self.mostrar_inventario).pack(fill="x", padx=10, pady=5)

        self.contenedor_principal = None
        self.mostrar_resumen()

    def cambiar_vista(self, vista_clase, *args, **kwargs):
        if self.contenedor_principal:
            self.contenedor_principal.destroy()
        
        self.contenedor_principal = vista_clase(self, *args, **kwargs)
        self.contenedor_principal.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

    def mostrar_resumen(self):
        self.cambiar_vista(ResumenView, self.db)

    def mostrar_inventario(self):
        self.cambiar_vista(InventarioView, self.db)

    def mostrar_ventas(self):
        # Pasamos el motor de ventas y una referencia para volver al resumen tras vender
        self.cambiar_vista(VentasView, self.ventas_motor, self.mostrar_resumen)