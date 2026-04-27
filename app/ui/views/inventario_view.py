import customtkinter as ctk

class InventarioView(ctk.CTkFrame):
    def __init__(self, parent, db):
        super().__init__(parent, corner_radius=15, fg_color="#0f0f0f")
        self.db = db
        self.renderizar()

    def renderizar(self):
        ctk.CTkLabel(self, text="Gestión de Inventario", font=("Orbitron", 22, "bold"), 
                    text_color="#a855f7").pack(pady=20, padx=20, anchor="w")

        tabla_frame = ctk.CTkScrollableFrame(self, fg_color="#121212", border_width=1, border_color="#3d0066")
        tabla_frame.pack(expand=True, fill="both", padx=20, pady=10)

        headers = ["ID", "Producto", "Precio", "Stock", "Categoría"]
        header_frame = ctk.CTkFrame(tabla_frame, fg_color="#1a1a1a")
        header_frame.pack(fill="x", pady=5)
        
        for i, h in enumerate(headers):
            ctk.CTkLabel(header_frame, text=h, font=("Segoe UI", 12, "bold"), width=120).grid(row=0, column=i, padx=10)

        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM productos")
            for prod in cursor.fetchall():
                fila = ctk.CTkFrame(tabla_frame, fg_color="transparent")
                fila.pack(fill="x", pady=2)
                for j, val in enumerate(prod):
                    ctk.CTkLabel(fila, text=str(val), width=120).grid(row=0, column=j, padx=10)