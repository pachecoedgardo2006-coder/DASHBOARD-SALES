import customtkinter as ctk
from tkinter import messagebox, ttk

class VentasView(ctk.CTkFrame):
    def __init__(self, parent, ventas_motor, al_vender_callback):
        super().__init__(parent, corner_radius=20, fg_color="#0a0a0a", border_width=1, border_color="#1a1a1a")
        self.ventas_motor = ventas_motor
        self.al_vender_callback = al_vender_callback
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.renderizar()

    def renderizar(self):
        # Header con estética "Dark Mystic"
        header = ctk.CTkLabel(self, text="PANEL DE CONTROL DE VENTAS", 
                             font=("Orbitron", 24, "bold"), text_color="#a855f7")
        header.grid(row=0, column=0, columnspan=2, pady=(20, 10), padx=20, sticky="w")

        # --- SECCIÓN IZQUIERDA: FORMULARIO (GLASSMORPHISM) ---
        form_container = ctk.CTkFrame(self, fg_color="#121212", border_width=1, border_color="#3d0066")
        form_container.grid(row=1, column=0, padx=20, pady=10, sticky="nsw")

        ctk.CTkLabel(form_container, text="Nueva Transacción", font=("JetBrains Mono", 16, "bold"), 
                    text_color="#e9d5ff").pack(pady=(15, 10), padx=20)

        self.id_input = ctk.CTkEntry(form_container, placeholder_text="ID del Producto", 
                                   width=220, height=40, fg_color="#0f0f0f", border_color="#6b21a8")
        self.id_input.pack(pady=10, padx=20)

        self.cant_input = ctk.CTkEntry(form_container, placeholder_text="Cantidad", 
                                     width=220, height=40, fg_color="#0f0f0f", border_color="#6b21a8")
        self.cant_input.pack(pady=10, padx=20)

        self.btn_venta = ctk.CTkButton(form_container, text="EJECUTAR VENTA", 
                                      font=("Orbitron", 13, "bold"), fg_color="#6b21a8", 
                                      hover_color="#9333ea", height=45, command=self.procesar_venta)
        self.btn_venta.pack(pady=20, padx=20, fill="x")

        # --- SECCIÓN DERECHA: KPIS Y TABLA ---
        stats_table_container = ctk.CTkFrame(self, fg_color="transparent")
        stats_table_container.grid(row=1, column=1, padx=(0, 20), pady=10, sticky="nsew")

        # Mini KPIs
        kpis = self.ventas_motor.obtener_kpis_ventas()
        kpi_frame = ctk.CTkFrame(stats_table_container, fg_color="transparent")
        kpi_frame.pack(fill="x", pady=(0, 10))

        self.crear_kpi_card(kpi_frame, "Hoy", kpis['ventas_hoy'], "#a855f7").pack(side="left", expand=True, padx=5)
        self.crear_kpi_card(kpi_frame, "Promedio", kpis['ticket_promedio'], "#7c3aed").pack(side="left", expand=True, padx=5)
        self.crear_kpi_card(kpi_frame, "Top", kpis['producto_top'], "#4c1d95").pack(side="left", expand=True, padx=5)

        # Tabla de Historial (Treeview con estilo personalizado)
        self.style_treeview()
        self.tree = ttk.Treeview(stats_table_container, columns=("ID", "Producto", "Cant", "Total", "Fecha"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Producto", text="PRODUCTO")
        self.tree.heading("Cant", text="CANT")
        self.tree.heading("Total", text="TOTAL")
        self.tree.heading("Fecha", text="FECHA")
        
        self.tree.column("ID", width=40, anchor="center")
        self.tree.column("Cant", width=50, anchor="center")
        self.tree.pack(fill="both", expand=True)
        self.actualizar_tabla()

    def crear_kpi_card(self, parent, title, value, color):
        card = ctk.CTkFrame(parent, fg_color="#121212", border_width=1, border_color=color, height=80)
        ctk.CTkLabel(card, text=title, font=("JetBrains Mono", 11), text_color="#9ca3af").pack(pady=(10, 0))
        ctk.CTkLabel(card, text=value, font=("JetBrains Mono", 14, "bold"), text_color=color).pack(pady=(0, 10), padx=10)
        return card

    def style_treeview(self):
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background="#0f0f0f", foreground="#e2e8f0", fieldbackground="#0f0f0f", borderwidth=0, font=("JetBrains Mono", 10), rowheight=35)
        style.configure("Treeview.Heading", background="#1a1a1a", foreground="#a855f7", font=("Orbitron", 10, "bold"), borderwidth=0)
        style.map("Treeview", background=[('selected', '#3d0066')])

    def actualizar_tabla(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for fila in self.ventas_motor.obtener_historial_reciente():
            self.tree.insert("", "end", values=fila)

    def procesar_venta(self):
        try:
            exito, mensaje = self.ventas_motor.procesar_venta(int(self.id_input.get()), int(self.cant_input.get()))
            if exito:
                messagebox.showinfo("Confirmación", mensaje)
                self.actualizar_tabla()
                self.al_vender_callback()
                self.id_input.delete(0, 'end')
                self.cant_input.delete(0, 'end')
            else:
                messagebox.showerror("Error de Venta", mensaje)
        except ValueError:
            messagebox.showwarning("Entrada Inválida", "Por favor, ingresa valores numéricos.")