import customtkinter as ctk
from tkinter import messagebox

class VentasView(ctk.CTkFrame):
    def __init__(self, parent, ventas_motor, al_vender_callback):
        super().__init__(parent, corner_radius=15, fg_color="#0f0f0f")
        self.ventas_motor = ventas_motor
        self.al_vender_callback = al_vender_callback
        self.renderizar()

    def renderizar(self):
        ctk.CTkLabel(self, text="Registrar Nueva Venta", font=("Orbitron", 22, "bold"), 
                    text_color="#a855f7").pack(pady=20, padx=20, anchor="w")

        form_frame = ctk.CTkFrame(self, fg_color="#121212", border_width=1, border_color="#3d0066")
        form_frame.pack(pady=10, padx=20, fill="x")

        self.id_input = ctk.CTkEntry(form_frame, placeholder_text="ID del Producto", width=200)
        self.id_input.pack(pady=10, padx=20)

        self.cant_input = ctk.CTkEntry(form_frame, placeholder_text="Cantidad a vender", width=200)
        self.cant_input.pack(pady=10, padx=20)

        ctk.CTkButton(form_frame, text="CONFIRMAR VENTA", fg_color="#6b21a8", 
                      command=self.procesar_venta).pack(pady=20)

    def procesar_venta(self):
        try:
            exito, mensaje = self.ventas_motor.procesar_venta(int(self.id_input.get()), int(self.cant_input.get()))
            if exito:
                messagebox.showinfo("Éxito", mensaje)
                self.al_vender_callback() # Llama a la función del Dashboard para refrescar
            else:
                messagebox.showerror("Error", mensaje)
        except ValueError:
            messagebox.showwarning("Error", "Ingresa números válidos.")