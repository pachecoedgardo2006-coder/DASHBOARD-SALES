import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import math
import threading
import time

# Importaciones de tu arquitectura base
from app.auth.auth_service import AuthService
from app.ui.views.dashboard_view import DashboardView


# ── Paleta de colores centralizada ────────────────────────────────────────────
COLORS = {
    "bg":           "#020202",
    "card":         "#080808",
    "card_border":  "#4c1d95",
    "input_bg":     "#0d0d0d",
    "input_border": "#252525",
    "accent":       "#a855f7",
    "accent_dark":  "#6b21a8",
    "accent_hover": "#7e22ce",
    "text_primary": "#f3e8ff",
    "text_muted":   "#71717a",
    "text_dim":     "#3f3f46",
    "text_node":    "#581c87",
}


class LoginView(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Servicios (capa lógica)
        self.auth_service = AuthService()

        # Configuración de la ventana
        self.title("NEON VAULT | SECURE ACCESS CONTROL")
        self.geometry("500x700")
        self.configure(fg_color=COLORS["bg"])
        self.resizable(False, False)

        # Estado de animación
        self.animating = True
        self._anim_step = 0.0

        # ── Fondo con orbes de luz ─────────────────────────────────────────
        self.bg_canvas = ctk.CTkCanvas(
            self,
            width=500,
            height=700,
            bg=COLORS["bg"],
            highlightthickness=0,
        )
        self.bg_canvas.place(x=0, y=0)
        self.bg_canvas.create_oval(-120, -120, 310, 320, fill="#12003a", outline="")
        self.bg_canvas.create_oval(290, 490, 620, 860, fill="#08082e", outline="")
        # Orbe central sutil
        self.bg_canvas.create_oval(150, 300, 350, 480, fill="#0e0020", outline="")

        # ── Glass card ────────────────────────────────────────────────────
        self.glass_card = ctk.CTkFrame(
            self,
            fg_color=COLORS["card"],
            border_width=2,
            border_color=COLORS["card_border"],
        )
        self.glass_card.place(
            relx=0.5, rely=0.5, anchor="center",
            relwidth=0.85, relheight=0.88,
        )

        self._build_header()
        self._build_inputs()
        self._build_actions()
        self._build_footer()

        # Animación iniciada DESPUÉS de construir todo
        self._start_glow_animation()

    # ── Secciones de UI ───────────────────────────────────────────────────────

    def _build_header(self):
        """Encabezado: línea de acento + título + indicador de estado."""
        # Línea de acento
        ctk.CTkFrame(
            self.glass_card,
            height=3,
            width=120,
            fg_color=COLORS["accent"],
            corner_radius=10,
        ).pack(pady=(45, 6))

        # Ícono / logotipo ASCII
        ctk.CTkLabel(
            self.glass_card,
            text="⬡",
            font=("Segoe UI Symbol", 36),
            text_color=COLORS["accent"],
        ).pack(pady=(0, 0))

        # Título principal
        ctk.CTkLabel(
            self.glass_card,
            text="DARK CORE",
            font=("Orbitron", 30, "bold"),
            text_color=COLORS["text_primary"],
        ).pack(pady=(6, 0))

        # Indicador de estado
        ctk.CTkLabel(
            self.glass_card,
            text="● SYSTEM ENCRYPTED",
            font=("Consolas", 10, "bold"),
            text_color=COLORS["accent"],
        ).pack(pady=(4, 32))

    def _build_inputs(self):
        """Campos de usuario y contraseña."""
        self.user_entry = self._labeled_entry(
            label="IDENTIFIER",
            placeholder="root@admin",
            show=None,
        )
        self.pass_entry = self._labeled_entry(
            label="SECURITY KEY",
            placeholder="••••••••••••",
            show="*",
        )

    def _labeled_entry(self, label: str, placeholder: str, show) -> ctk.CTkEntry:
        """Crea un bloque etiqueta + campo con efecto focus."""
        frame = ctk.CTkFrame(self.glass_card, fg_color="transparent")
        frame.pack(pady=10, padx=40, fill="x")

        ctk.CTkLabel(
            frame,
            text=label,
            font=("Orbitron", 9, "bold"),
            text_color=COLORS["accent"],
        ).pack(anchor="w", padx=4, pady=(0, 5))

        entry = ctk.CTkEntry(
            frame,
            placeholder_text=placeholder,
            show=show,
            height=52,
            fg_color=COLORS["input_bg"],
            border_color=COLORS["input_border"],
            text_color=COLORS["text_primary"],
            placeholder_text_color="#444",
            font=("Segoe UI", 14),
            corner_radius=12,
        )
        entry.pack(fill="x")
        entry.bind("<FocusIn>",  lambda e: entry.configure(border_color=COLORS["accent"]))
        entry.bind("<FocusOut>", lambda e: entry.configure(border_color=COLORS["input_border"]))
        entry.bind("<Return>",   lambda e: self._ejecutar_login())
        return entry

    def _build_actions(self):
        """Botón principal de login y botón secundario de recuperación."""
        container = ctk.CTkFrame(self.glass_card, fg_color="transparent")
        container.pack(pady=(30, 0), padx=40, fill="x")

        self.login_button = ctk.CTkButton(
            container,
            text="INITIALIZE SESSION",
            font=("Orbitron", 13, "bold"),
            text_color="#ffffff",
            height=58,
            fg_color=COLORS["accent_dark"],
            hover_color=COLORS["accent_hover"],
            corner_radius=14,
            border_width=2,
            border_color=COLORS["accent"],
            command=self._ejecutar_login,
        )
        self.login_button.pack(fill="x", pady=(0, 12))

        ctk.CTkButton(
            container,
            text="FORGOT ACCESS KEY?",
            font=("Orbitron", 9),
            text_color=COLORS["text_muted"],
            fg_color="transparent",
            hover_color="#141414",
            height=28,
            command=self._recovery_stub,
        ).pack(fill="x")

    def _build_footer(self):
        """Footer con info de encriptación y versión."""
        footer = ctk.CTkFrame(self.glass_card, fg_color="transparent")
        footer.pack(side="bottom", pady=28)

        ctk.CTkLabel(
            footer,
            text="AES-256 BIT ENCRYPTION ACTIVE",
            font=("Consolas", 9),
            text_color=COLORS["text_dim"],
        ).pack()

        ctk.CTkLabel(
            footer,
            text="NODE: 192.168.1.104  |  BUILD: 2026.4",
            font=("Consolas", 9),
            text_color=COLORS["text_node"],
        ).pack(pady=(2, 0))

    # ── Animaciones ───────────────────────────────────────────────────────────

    def _start_glow_animation(self):
        """Pulso suave del borde de la card usando .after() (thread-safe)."""
        def _tick():
            if not self.animating:
                return
            val = int(90 + 60 * math.sin(self._anim_step))   # rango 30-150
            # Componente rojo/azul controlada para no salir de rango válido
            r = min(255, val)
            b = min(255, val)
            color = f"#{r:02x}00{b:02x}"
            try:
                self.glass_card.configure(border_color=color)
            except Exception:
                return
            self._anim_step += 0.04
            self.after(80, _tick)

        self.after(100, _tick)

    # ── Lógica de autenticación ───────────────────────────────────────────────

    def _ejecutar_login(self):
        """Valida campos y dispara el proceso de autenticación."""
        user     = self.user_entry.get().strip()
        password = self.pass_entry.get()

        if not user or not password:
            messagebox.showwarning(
                "AUTH ERROR",
                "All links must be populated.",
            )
            return

        self.login_button.configure(state="disabled", text="VERIFYING…")
        self.update_idletasks()
        self.after(900, lambda: self._process_auth(user, password))

    def _process_auth(self, user: str, password: str):
        """Llama al AuthService y actúa según el resultado."""
        if self.auth_service.login(user, password):
            self.animating = False
            self.withdraw()
            self._abrir_dashboard()
        else:
            messagebox.showerror(
                "ACCESS DENIED",
                "Invalid credentials. Protocol rejected.",
            )
            self._reset_button()

    def _reset_button(self):
        self.login_button.configure(state="normal", text="INITIALIZE SESSION")

    def _recovery_stub(self):
        """Placeholder para flujo de recuperación."""
        messagebox.showinfo("RECOVERY", "Recovery protocol initiated.")

    def _abrir_dashboard(self):
        """Instancia y lanza DashboardView."""
        try:
            self.dash_window = DashboardView()
            self.dash_window.protocol("WM_DELETE_WINDOW", self._cerrar_todo)
            self.dash_window.mainloop()
        except Exception as exc:
            messagebox.showerror("SYSTEM ERROR", f"Failed to initialize dashboard:\n{exc}")
            self.deiconify()
            self._reset_button()

    def _cerrar_todo(self):
        """Cierre limpio: detiene animaciones y destruye ventanas."""
        self.animating = False
        if hasattr(self, "dash_window"):
            self.dash_window.destroy()
        self.destroy()


# ── Entry point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    app = LoginView()
    app.mainloop()