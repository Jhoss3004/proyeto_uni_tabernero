import tkinter as tk
from tkinter import ttk, messagebox as msg
from PIL import Image, ImageTk
from typing import Any

from pathlib import Path

BASE = Path(__file__).resolve().parent.parent

ESTILO_BOTON = dict[str, Any](
    bg="#4e3525",
    fg="#D7A36B",
    activebackground="#3A2719",
    activeforeground="#D7A36B",
    relief="flat",
    bd=0,
    highlightthickness=0,
    cursor="hand2"
)

class TabernaVista:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("La Taberna")
        self.ventana.geometry("960x540+290+130")
        self.ventana.resizable(False,False)

        self._configurar_estilos()
        self._crear_fondo()
        self._crear_widgets()

    def _configurar_estilos(self):
        estilo = ttk.Style()
        estilo.theme_use("clam")
        estilo.configure(
            "Taberna.Vertical.TScrollbar",
            troughcolor="#C78D5D",
            background="#4B2C18",
            bordercolor="#C78D5D",
            lightcolor="#4B2C18",
            darkcolor="#4B2C18",
            arrowcolor="#C78D5D",
            arrowsize=5,
            gripcount=0
        )
        estilo.map(
            "Taberna.Vertical.TScrollbar",
            background=[("active","#2B120B"),("pressed", "#2B120B")]
        )
        estilo.layout("Taberna.Vertical.TScrollbar", [
            ("Vertical.Scrollbar.trough", {
                    "sticky": "ns",
                    "children": [
                        ("Vertical.Scrollbar.thumb", {
                            "sticky": "nswe"
                        })
                    ]
                })
            ]
        )

    def _crear_fondo(self):
        imagen = Image.open(BASE / "fondo.jpg").resize((960, 540))
        self.imagen_fondo = ImageTk.PhotoImage(imagen)

        self.icono = tk.PhotoImage(file=BASE / "icono.png")
        self.ventana.iconphoto(True, self.icono)

        tk.Label(self.ventana, image=self.imagen_fondo).place(x=0, y=0, relwidth=1, relheight=1)

    def _crear_widgets(self):
        fuente_medieval = ("Old English Text MT", 14, "bold")
        fuente_entrada = ("Georgia", 12, "bold")

        panel = tk.Frame(
            self.ventana,
            width=440,
            height=230,
            bg="#8B5A2B",
            highlightbackground="#4B2C18",
            highlightthickness=3,
            bd=0
        )
        panel.place(x=20, y=20)

        self.cuadro_tabernero = tk.Text(
            panel,
            height=8,
            width=45,
            wrap=tk.WORD,
            borderwidth=0,
            bg="#C78D5D",
            fg="#2B120B",
            relief="flat",
            padx=16,
            pady=12,
            font=fuente_medieval,
            state=tk.DISABLED,
            cursor="arrow",
            spacing1=4,
            spacing2=4,
            spacing3=4
        )
        self.cuadro_tabernero.pack(side="left", fill="both", expand=True)

        scroll = ttk.Scrollbar(
            panel,
            orient="vertical",
            command=self.cuadro_tabernero.yview,
            style="Taberna.Vertical.TScrollbar"
        )
        scroll.pack(side="right", fill="y")
        self.cuadro_tabernero.config(yscrollcommand=scroll.set)

        self.cuadro_texto = tk.Text(
            self.ventana,
            height=4,
            width=33,
            wrap=tk.WORD,
            borderwidth=0,
            bg="#D7A36B",
            fg="#2B120B",
            insertbackground="#2B120B",
            relief="flat",
            padx=14,
            pady=10,
            font=fuente_entrada,
            highlightthickness=2,
            highlightbackground="#7A4A2A",
            highlightcolor="#7A4A2A"
        )
        self.cuadro_texto.place(x=20, y=400, relwidth=0.8)
        self.cuadro_texto.focus_set()
        self.cuadro_texto.bind("<Shift-Return>", self._salto_linea)
        self.cuadro_texto.bind("<Shift-KP_Enter>", self._salto_linea)

        self.boton_enviar = tk.Button(self.ventana, text="Enviar", width=10, **ESTILO_BOTON)
        self.boton_enviar.place(x=20, y=510)

        self.boton_limpiar = tk.Button(self.ventana, text="Limpiar", width=10, **ESTILO_BOTON)
        self.boton_limpiar.place(x=100, y=510)

    def _salto_linea(self, event=None):
        self.cuadro_texto.insert(tk.INSERT, "\n")
        return "break"

    """ ---------- Metodos para el controlador ---------- """

    def obtener_texto(self):
        return self.cuadro_texto.get("1.0", tk.END).strip()

    def limpiar_entrada(self):
        self.cuadro_texto.delete("1.0", tk.END)

    def mostrar_respuesta(self, respuesta):
        self.cuadro_tabernero.configure(state=tk.NORMAL)
        self.cuadro_tabernero.delete("1.0", tk.END)
        self.cuadro_tabernero.insert("1.0", respuesta)
        self.cuadro_tabernero.configure(state=tk.DISABLED)

    def bloquear_envio(self):
        self.boton_enviar.config(state=tk.DISABLED)

    def habilitar_envio(self):
        self.boton_enviar.config(state=tk.NORMAL)
        self.cuadro_texto.focus_set()

    def advertir(self, titulo, mensaje):
        msg.showwarning(title=titulo, message=mensaje)

    def confirmar_salida(self, al_confirmar):
        dialogo = tk.Toplevel(self.ventana)
        dialogo.title("Salir")
        dialogo.configure(bg="#C78D5D", padx=20, pady=15)
        dialogo.resizable(False, False)
        dialogo.transient(self.ventana)
        dialogo.grab_set()
        dialogo.focus_set()

        tk.Label(
            dialogo, text="¿Seguro que deseas abandonar la taberna?",
            bg="#C78D5D", fg="#2B120B", font=("Georgia", 12, "bold")
        ).pack(pady=(0, 15))

        botones = tk.Frame(dialogo, bg="#C78D5D")
        botones.pack()
        tk.Button(botones, text="Si", width=8, command=al_confirmar, **ESTILO_BOTON).pack(side="left", padx=5)
        tk.Button(botones, text="No", width=8, command=dialogo.destroy, **ESTILO_BOTON).pack(side="left", padx=5)

        dialogo.bind("<Escape>", lambda e: dialogo.destroy())
        dialogo.bind("<Return>", lambda e: al_confirmar())
        dialogo.bind("<KP_Enter>", lambda e: al_confirmar())

        dialogo.update_idletasks()
        x = self.ventana.winfo_x() + (self.ventana.winfo_width() - dialogo.winfo_width()) // 2
        y = self.ventana.winfo_y() + (self.ventana.winfo_height() - dialogo.winfo_height()) // 2
        dialogo.geometry(f"+{x}+{y}")