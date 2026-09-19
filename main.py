import sys
import ctypes
import tkinter as tk

from ia.conexion import crear_chat
from models.modelo import TabernaModelo
from views.principal import TabernaVista
from controllers.controlador import TabernaControlador

if sys.platform == "win32":
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("uptaiet.taberna")

ventana = tk.Tk()
modelo = TabernaModelo(crear_chat())
vista = TabernaVista(ventana)
controlador = TabernaControlador(modelo, vista)
ventana.mainloop()
