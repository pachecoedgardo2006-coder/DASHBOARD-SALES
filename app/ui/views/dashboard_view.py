import customtkinter as ctk
from app.database.db_config import Database
from app.ventas.ventas_logic import VentasLogic

class DashboardView(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.db = Database()
        self.title("Dark Mystic - Sales System")
        self.geometry("1100x600")
        self.configure(fg_color="#0a0a0a")
        self.ventas_motor = VentasLogic() # Instanciar la lógica de ventas

        # Configuración de Layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- SIDEBAR (Menú Único) ---
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0, fg_color="#121212")
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        self.logo_label = ctk.CTkLabel(self.sidebar, text="DASHBOARD", font=("Orbitron", 20, "bold"), text_color="#a855f7")
        self.logo_label.pack(pady=30, padx=20)

        # Botón Resumen
        self.btn_resumen = ctk.CTkButton(self.sidebar, text="🏠  Resumen", anchor="w", 
                                        fg_color="transparent", hover_color="#1e1e1e",
                                        command=self.renderizar_resumen)
        self.btn_resumen.pack(fill="x", padx=10, pady=5)

        # Botón Ventas (Lo conectaremos pronto)
        self.btn_ventas = ctk.CTkButton(self.sidebar, text="💰  Ventas", anchor="w", 
                                       fg_color="transparent", hover_color="#1e1e1e",
                                       command=self.renderizar_ventas) # Crea este método vacío o con un pass
        self.btn_ventas.pack(fill="x", padx=10, pady=5)

        # Botón Inventario
        self.btn_inventario = ctk.CTkButton(self.sidebar, text="📦  Inventario", anchor="w", 
                                            fg_color="transparent", hover_color="#1e1e1e",
                                            command=self.renderizar_inventario)
        self.btn_inventario.pack(fill="x", padx=10, pady=5)

        # --- MAIN CONTENT ---
        self.main_content = ctk.CTkFrame(self, corner_radius=15, fg_color="#0f0f0f")
        self.main_content.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

        # Ejecutar la renderización inicial
        self.renderizar_resumen()

    def crear_componente_stats(self, parent, titulo, valor, color):
        """Función única para crear tarjetas de estadísticas."""
        card = ctk.CTkFrame(parent, fg_color="#121212", border_width=2, border_color=color, corner_radius=15)
        ctk.CTkLabel(card, text=titulo, font=("Orbitron", 10, "bold"), text_color="gray").pack(pady=(15, 0))
        ctk.CTkLabel(card, text=valor, font=("Orbitron", 28, "bold"), text_color="white").pack(pady=(5, 15))
        return card

    def renderizar_resumen(self):
        """Limpia el área principal y muestra las estadísticas reales."""
        # Limpiar contenido previo
        for widget in self.main_content.winfo_children():
            widget.destroy()

        # Título de sección
        ctk.CTkLabel(self.main_content, text="Panel de Control", font=("Orbitron", 22, "bold"), text_color="#a855f7").pack(pady=20, padx=20, anchor="w")

        # Obtener datos de la DB (usamos el método que ya tienes en db_config)
        total_dinero, total_stock = self.db.get_resumen_dashboard()

        # Frame para las tarjetas
        stats_container = ctk.CTkFrame(self.main_content, fg_color="transparent")
        stats_container.pack(fill="x", padx=20)

        # Crear tarjetas usando la función unificada
        self.crear_componente_stats(stats_container, "INGRESOS TOTALES", f"${total_dinero:.2f}", "#6b21a8").pack(side="left", padx=10, expand=True, fill="both")
        self.crear_componente_stats(stats_container, "PRODUCTOS EN STOCK", f"{total_stock}", "#3d0066").pack(side="left", padx=10, expand=True, fill="both")
    
    def renderizar_inventario(self):
        """Muestra la lista de productos actual en la DB."""
        # 1. Limpiar pantalla
        for widget in self.main_content.winfo_children():
            widget.destroy()

        # 2. Título
        ctk.CTkLabel(self.main_content, text="Gestión de Inventario", 
                    font=("Orbitron", 22, "bold"), text_color="#a855f7").pack(pady=20, padx=20, anchor="w")

        # 3. Frame para la tabla
        tabla_frame = ctk.CTkScrollableFrame(self.main_content, fg_color="#121212", 
                                            border_width=1, border_color="#3d0066")
        tabla_frame.pack(expand=True, fill="both", padx=20, pady=10)

        # Encabezados
        headers = ["ID", "Producto", "Precio", "Stock", "Categoría"]
        header_frame = ctk.CTkFrame(tabla_frame, fg_color="#1a1a1a")
        header_frame.pack(fill="x", pady=5)
        
        for i, h in enumerate(headers):
            ctk.CTkLabel(header_frame, text=h, font=("Segoe UI", 12, "bold"), width=120).grid(row=0, column=i, padx=10)

        # 4. Obtener datos reales de la DB
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM productos")
            productos = cursor.fetchall()

        # 5. Dibujar filas
        for i, prod in enumerate(productos):
            fila = ctk.CTkFrame(tabla_frame, fg_color="transparent")
            fila.pack(fill="x", pady=2)
            for j, val in enumerate(prod):
                ctk.CTkLabel(fila, text=str(val), width=120).grid(row=0, column=j, padx=10)


    def renderizar_ventas(self):
        """Formulario para procesar una venta en tiempo real."""
        for widget in self.main_content.winfo_children():
            widget.destroy()

        ctk.CTkLabel(self.main_content, text="Registrar Nueva Venta", 
                    font=("Orbitron", 22, "bold"), text_color="#a855f7").pack(pady=20, padx=20, anchor="w")

        # Contenedor del formulario
        form_frame = ctk.CTkFrame(self.main_content, fg_color="#121212", border_width=1, border_color="#3d0066")
        form_frame.pack(pady=10, padx=20, fill="x")

        # Campo ID Producto
        self.id_input = ctk.CTkEntry(form_frame, placeholder_text="ID del Producto", width=200)
        self.id_input.pack(pady=10, padx=20)

        # Campo Cantidad
        self.cant_input = ctk.CTkEntry(form_frame, placeholder_text="Cantidad a vender", width=200)
        self.cant_input.pack(pady=10, padx=20)

        # Botón de Procesar
        btn_vender = ctk.CTkButton(form_frame, text="CONFIRMAR VENTA", fg_color="#6b21a8", command=self.procesar_venta_ui)
        btn_vender.pack(pady=20)

    def procesar_venta_ui(self):
        """Ejecuta la venta y actualiza el Dashboard automáticamente."""
        try:
            prod_id = int(self.id_input.get())
            cantidad = int(self.cant_input.get())
            
            # Ejecutar la lógica de negocio
            exito, mensaje = self.ventas_motor.procesar_venta(prod_id, cantidad)
            
            if exito:
                # Feedback visual y retorno al resumen con datos frescos
                from tkinter import messagebox
                messagebox.showinfo("Éxito", mensaje)
                self.renderizar_resumen() # Refresca los totales inmediatamente
            else:
                from tkinter import messagebox
                messagebox.showerror("Error de Venta", mensaje)
                
        except ValueError:
            from tkinter import messagebox
            messagebox.showwarning("Entrada Inválida", "Por favor ingresa números válidos.")