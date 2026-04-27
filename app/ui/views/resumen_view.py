import customtkinter as ctk
from app.ui.components.stats_card import StatsCard

class ResumenView(ctk.CTkFrame):
    def __init__(self, parent, db):
        super().__init__(parent, corner_radius=15, fg_color="#0f0f0f")
        self.db = db
        self.renderizar()

    def renderizar(self):
        ctk.CTkLabel(self, text="Panel de Control", font=("Orbitron", 22, "bold"), 
                    text_color="#a855f7").pack(pady=20, padx=20, anchor="w")

        total_dinero, total_stock = self.db.get_resumen_dashboard()

        stats_container = ctk.CTkFrame(self, fg_color="transparent")
        stats_container.pack(fill="x", padx=20)

        StatsCard(stats_container, "INGRESOS TOTALES", f"${total_dinero:.2f}", "#6b21a8").pack(side="left", padx=10, expand=True, fill="both")
        StatsCard(stats_container, "PRODUCTOS EN STOCK", f"{total_stock}", "#3d0066").pack(side="left", padx=10, expand=True, fill="both")