# app/ui/views/inventario_view.py

import customtkinter as ctk
from tkinter import ttk
import sys
import os

# Asegurar que el path de la app sea reconocido en Linux
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))

class InventarioView(ctk.CTkFrame):
    def __init__(self, parent, db):
        super().__init__(parent, corner_radius=15, fg_color="#0b0b12")
        self.db = db
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.renderizar()

    def renderizar(self):
        # Header
        header_container = ctk.CTkFrame(self, fg_color="transparent")
        header_container.pack(fill="x", padx=25, pady=(20, 10))

        ctk.CTkLabel(
            header_container, 
            text="SYSTEM_INVENTORY_CORE", 
            font=("Orbitron", 24, "bold"), 
            text_color="#a855f7"
        ).pack(side="left")

        # Dashboard de KPIs (Contenedor)
        self.stats_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.stats_frame.pack(fill="x", padx=20, pady=10)
        
        # LLAMADA AL MÉTODO QUE DABA ERROR
        self.crear_kpis()

        # Herramientas
        self.tools_frame = ctk.CTkFrame(self, fg_color="#161625", corner_radius=10, border_width=1, border_color="#3d0066")
        self.tools_frame.pack(fill="x", padx=25, pady=10)
        
        self.search_entry = ctk.CTkEntry(self.tools_frame, placeholder_text="Buscar producto...", width=300, fg_color="#0f0f1a", border_color="#581c87")
        self.search_entry.pack(side="left", padx=15, pady=10)

        ctk.CTkButton(self.tools_frame, text="+ Nuevo Item", fg_color="#6d28d9", hover_color="#4c1d95", font=("Segoe UI", 12, "bold"), width=120).pack(side="right", padx=15)

        # Tabla
        self.contenedor_tabla = ctk.CTkFrame(self, fg_color="#0f0f1a", corner_radius=12, border_width=1, border_color="#1e1b4b")
        self.contenedor_tabla.pack(expand=True, fill="both", padx=25, pady=(5, 25))

        self.setup_tabla_estilizada()
        self.actualizar_datos_tabla()

    def crear_kpis(self):
        """Metodo para obtener y mostrar metricas reales"""
        try:
            try:
                from app.inventory.inventory_manager import InventoryManager
            except ImportError:
                from inventory.inventory_manager import InventoryManager
            
            manager = InventoryManager()
            stats = manager.obtener_metricas_globales()
            
            metrics = [
                ("Total Productos", str(stats['total_items']), "#a855f7"),
                ("Stock Bajo", str(stats['stock_bajo']), "#ef4444"),
                ("Valor Total", f"${stats['valor_total']:,.2f}", "#22c55e")
            ]
        except Exception:
            metrics = [("Total Productos", "0", "#a855f7"), ("Stock Bajo", "0", "#ef4444"), ("Valor Total", "$0.00", "#22c55e")]

        for widget in self.stats_frame.winfo_children():
            widget.destroy()

        for label, val, color in metrics:
            card = ctk.CTkFrame(self.stats_frame, fg_color="#161625", width=180, height=80, corner_radius=12, border_width=1, border_color="#3d0066")
            card.pack(side="left", padx=10, expand=True, fill="both")
            card.pack_propagate(False)
            ctk.CTkLabel(card, text=label, font=("Segoe UI", 11), text_color="#94a3b8").pack(pady=(10, 0))
            ctk.CTkLabel(card, text=val, font=("Orbitron", 18, "bold"), text_color=color).pack()

    def setup_tabla_estilizada(self):
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background="#0f0f1a", foreground="white", fieldbackground="#0f0f1a", borderwidth=0, font=("Segoe UI", 11), rowheight=35)
        style.configure("Treeview.Heading", background="#1e1b4b", foreground="#a855f7", font=("Orbitron", 10, "bold"), borderwidth=0)
        style.map("Treeview", background=[('selected', '#3d0066')])

        columnas = ("id", "nombre", "precio", "stock", "categoria", "estado")
        self.tree = ttk.Treeview(self.contenedor_tabla, columns=columnas, show='headings', selectmode="browse")
        
        headers = {"id": "ID", "nombre": "PRODUCTO", "precio": "PRECIO", "stock": "CANTIDAD", "categoria": "CATEGORÍA", "estado": "STATUS"}
        for col, text in headers.items():
            self.tree.heading(col, text=text)
            self.tree.column(col, anchor="center", width=100)

        self.scrollbar = ctk.CTkScrollbar(self.contenedor_tabla, orientation="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scrollbar.set)
        self.tree.pack(side="left", expand=True, fill="both", padx=10, pady=10)
        self.scrollbar.pack(side="right", fill="y", padx=(0, 10), pady=10)

    def actualizar_datos_tabla(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        try:
            with self.db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM productos")
                for prod in cursor.fetchall():
                    stock = prod[3]
                    estado = "🟢 Óptimo" if stock > 10 else "🟠 Bajo" if stock > 0 else "🔴 Agotado"
                    self.tree.insert("", "end", values=(prod[0], prod[1], f"${prod[2]:,.2f}", prod[3], prod[4], estado))
        except Exception:
            pass