import customtkinter as ctk

class StatsCard(ctk.CTkFrame):
    def __init__(self, parent, titulo, valor, color):
        # Fondo oscuro con borde de color neón
        super().__init__(parent, fg_color="#121212", border_width=1, border_color=color, corner_radius=15)
        
        # Título en gris suave para contraste
        ctk.CTkLabel(self, text=titulo, font=("Orbitron", 10, "bold"), text_color="#94a3b8").pack(pady=(15, 0))
        
        # Valor principal resaltado
        ctk.CTkLabel(self, text=valor, font=("Orbitron", 28, "bold"), text_color="white").pack(pady=(5, 10))
        
        # Línea de detalle inferior (Glow effect)
        ctk.CTkFrame(self, fg_color=color, height=3, width=60, corner_radius=10).pack(pady=(0, 15))