import tkinter as tk
from tkinter import messagebox
import threading
from vehiculo import Vehiculo

class CarreraMecatronica:
    def __init__(self, root):
        self.root = root
        self.root.title("Carrera Mecatronica")
        self.root.geometry("1000x650")

        self.nombres = [
            "Carro 1", "Carro 2", "Carro 3", "Carro 4", "Carro 5",
            "Carro 6", "Carro 7", "Carro 8", "Carro 9", "Carro 10"
        ]

        self.colores = [
            "red", "blue", "green", "white", "orange",
            "yellow", "black", "purple", "gray", "pink"
        ]

        self.vehiculos = []
        self.en_carrera = False
        self.configurar_interfaz()

    def configurar_interfaz(self):
        panel = tk.Frame(self.root, bg="#03111f", pady=15)
        panel.pack(side=tk.TOP, fill=tk.X)

        tk.Label(panel, text="Apuesta:", bg="#03111f", fg="white").grid(row=0, column=0, padx=5)
        self.combo_apuesta = tk.StringVar(value=self.nombres[0])
        tk.OptionMenu(panel, self.combo_apuesta, *self.nombres).grid(row=0, column=1)

        tk.Label(panel, text="Rondas:", bg="#03111f", fg="white").grid(row=0, column=2, padx=5)
        self.var_vueltas = tk.IntVar(value=1)
        tk.Spinbox(panel, from_=1, to=5, textvariable=self.var_vueltas, width=5).grid(row=0, column=3)

        tk.Label(panel, text="Velocidad:", bg="#03111f", fg="white").grid(row=0, column=4, padx=5)
        self.slider_vel = tk.Scale(panel, from_=10, to=100, orient=tk.HORIZONTAL, bg="#03111f", fg="white")
        self.slider_vel.set(70)
        self.slider_vel.grid(row=0, column=5)

        self.btn_go = tk.Button(panel, text="INICIAR", command=self.comenzar)
        self.btn_go.grid(row=0, column=6, padx=20)

        self.pista = tk.Frame(self.root, bg="#34495e")
        self.pista.pack(fill=tk.BOTH, expand=True)
        tk.Frame(self.pista, bg="#ecf0f1", width=10).place(x=980, y=40, height=580)

        self.preparar_pista()

    def preparar_pista(self):
        for v in self.vehiculos:
            v.widget.destroy()
        self.vehiculos.clear()

        for i in range(10):
            lbl = tk.Label(self.pista, text=self.nombres[i], bg=self.colores[i], width=18, height=2)
            lbl.place(x=0, y=i * 60 + 60)


            v = Vehiculo(i, self.nombres[i], self.colores[i], lbl, self)
            self.vehiculos.append(v)

    def comenzar(self):
        if self.en_carrera:
            return
        self.en_carrera = True
        self.btn_go.config(state=tk.DISABLED)
        self.preparar_pista()

        for v in self.vehiculos:
            v.start()


        hilo_control = threading.Thread(target=self.esperar_finalizacion, daemon=True)
        hilo_control.start()

    def esperar_finalizacion(self):

        for v in self.vehiculos:
            v.join() 

        self.root.after(0, self.mostrar_resultados)

    def mostrar_resultados(self):
        self.en_carrera = False
        self.btn_go.config(state=tk.NORMAL)

        ranking = sorted(self.vehiculos, key=lambda v: v.tiempo_fin - v.tiempo_inicio)

        resultado = "PODIO FINAL\n\n"
        apuesta = self.combo_apuesta.get()
        for pos, v in enumerate(ranking, 1):
            tiempo = v.tiempo_fin - v.tiempo_inicio
            resultado += f"{pos}. {v.nombre}: {tiempo:.3f}s\n"

        ganador = ranking[0].nombre
        if apuesta == ganador:
            resultado += f"\nApuesta a {apuesta}: GANASTE!"
        else:
            resultado += f"\nApuesta a {apuesta}: perdiste. Gano {ganador}."

        messagebox.showinfo("Resultados", resultado)
