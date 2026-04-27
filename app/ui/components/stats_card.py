import customtkinter as ctk

class StatsCard(ctk.CTkFrame):
    def __init__(self, parent, titulo, valor, color):
        super().__init__(parent, fg_color="#121212", border_width=2, border_color=color, corner_radius=15)
        
        ctk.CTkLabel(self, text=titulo, font=("Orbitron", 10, "bold"), text_color="gray").pack(pady=(15, 0))
        ctk.CTkLabel(self, text=valor, font=("Orbitron", 28, "bold"), text_color="white").pack(pady=(5, 15))