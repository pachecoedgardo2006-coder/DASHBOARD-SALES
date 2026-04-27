import customtkinter as ctk
from app.ui.components.stats_card import StatsCard

class ResumenView(ctk.CTkFrame):
    def __init__(self, parent, db):
        super().__init__(parent, corner_radius=15, fg_color="#0f0f0f")
        self.db = db
        self.renderizar()

    def renderizar(self):
        # Header Estilo Cyberpunk
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", pady=(20, 10), padx=25)
        
        ctk.CTkLabel(header_frame, text="TERMINAL_RESUMEN_SISTEMA", font=("Orbitron", 22, "bold"), 
                    text_color="#a855f7").pack(side="left")

        # Obtener datos (Asumiendo que actualices db_config más adelante)
        # Por ahora usamos los que ya tienes y añadimos placeholders
        total_dinero, total_stock = self.db.get_resumen_dashboard()
        
        # Contenedor de Cards
        stats_container = ctk.CTkFrame(self, fg_color="transparent")
        stats_container.pack(fill="x", padx=15, pady=10)

        StatsCard(stats_container, "INGRESOS TOTALES", f"${total_dinero:,.2f}", "#7e22ce").pack(side="left", padx=10, expand=True, fill="both")
        StatsCard(stats_container, "UNIDADES STOCK", f"{total_stock}", "#4c1d95").pack(side="left", padx=10, expand=True, fill="both")
        StatsCard(stats_container, "PRODUCTOS BAJO STOCK", "5", "#dc2626").pack(side="left", padx=10, expand=True, fill="both")

        # Cuerpo del Dashboard (Dos columnas)
        main_body = ctk.CTkFrame(self, fg_color="transparent")
        main_body.pack(fill="both", expand=True, padx=25, pady=10)

        # Columna Izquierda: Actividad Reciente
        self.crear_log_actividad(main_body)

    def crear_log_actividad(self, parent):
        log_frame = ctk.CTkFrame(parent, fg_color="#121212", border_width=1, border_color="#1e1e1e")
        log_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        ctk.CTkLabel(log_frame, text=" > ACTIVIDAD_RECIENTE_ ", font=("Consolas", 14), 
                    text_color="#a855f7").pack(pady=10, padx=15, anchor="w")
        
        # Simulando datos de la DB
        logs = [
            "2026-04-27 15:30 | VENTA REALIZADA #459",
            "2026-04-27 14:15 | STOCK ACTUALIZADO: Monitor Pro",
            "2026-04-27 12:00 | NUEVO USUARIO REGISTRADO"
        ]
        
        for log in logs:
            ctk.CTkLabel(log_frame, text=log, font=("Consolas", 11), text_color="#64748b").pack(padx=20, anchor="w")