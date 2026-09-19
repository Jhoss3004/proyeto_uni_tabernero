import threading


class TabernaControlador:
    def __init__(self, modelo, vista):
        self.modelo = modelo
        self.vista = vista
        self.esperando = False

        self.vista.boton_enviar.config(command=self.enviar)
        self.vista.boton_limpiar.config(command=self.reiniciar)
        self.vista.cuadro_texto.bind("<Return>", self.enviar)
        self.vista.cuadro_texto.bind("<KP_Enter>", self.enviar)
        self.vista.ventana.protocol("WM_DELETE_WINDOW", self.salir)
        self.vista.ventana.bind("<Escape>", lambda e: self.salir())

        self.vista.mostrar_respuesta(self.modelo.BIENVENIDA)

    def enviar(self, event=None):
        texto = self.vista.obtener_texto()
        if not texto:
            self.vista.advertir("¡Pero Preguntad Algo!", "¿A caso solo entraste a ver?")
            return "break"
        if self.esperando:
            self.vista.advertir("¡Un momento!", "Dejadme Pensar...")
            return "break"

        self.esperando = True
        self.limpiar()
        self.vista.bloquear_envio()
        self.vista.mostrar_respuesta(self.modelo.PENSANDO)

        threading.Thread(target=self._consultar, args=(texto,), daemon=True).start()
        return "break"

    def _consultar(self, texto):
        resultado = self.modelo.preguntar(texto)
        self.vista.ventana.after(0, self.vista.mostrar_respuesta, resultado)
        self.modelo.hablar(resultado)
        self.vista.ventana.after(0, self._terminar_espera)

    def _terminar_espera(self):
        self.esperando = False
        self.vista.habilitar_envio()

    def reiniciar(self):
        self.vista.limpiar_entrada()
        self.modelo.detener_voz()
        self.vista.mostrar_respuesta(self.modelo.BIENVENIDA)

    def limpiar(self):
        self.vista.limpiar_entrada()

    def salir(self):
        self.vista.confirmar_salida(self.vista.ventana.destroy)
