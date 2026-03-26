import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time

class Tarea:
    def __init__(self, tipo, tiempo):
        self.tipo = tipo
        self.tiempo = tiempo # Ahora se forzará a entero

class PilaTareas:
    def __init__(self):
        self.items = []
        self.lock = threading.Lock()

    def apilar(self, item):
        with self.lock:
            self.items.append(item)

    def desapilar(self):
        with self.lock:
            if not self.esta_vacia():
                return self.items.pop() 
            return None

    def esta_vacia(self):
        return len(self.items) == 0

    def obtener_tipos(self):
        return [tarea.tipo for tarea in self.items]

class AppRobot:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador Robot Explorador (Pila)")
        self.root.geometry("350x400")
        self.pila = PilaTareas()
        self.procesador_ocupado = False

        self.configurar_interfaz()

    def configurar_interfaz(self):
        # Marco para ingreso de datos
        frame_datos = tk.Frame(self.root)
        frame_datos.pack(pady=10)

        tk.Label(frame_datos, text="Tipo de Tarea:").grid(row=0, column=0, sticky="e")
        self.combo_tipo = ttk.Combobox(frame_datos, values=["Sensores", "Movimiento"], state="readonly")
        self.combo_tipo.current(0)
        self.combo_tipo.grid(row=0, column=1, padx=5)

        tk.Label(frame_datos, text="Tiempo de ejecución (s enteros):").grid(row=1, column=0, sticky="e")
        self.entrada_tiempo = tk.Entry(frame_datos, width=10)
        self.entrada_tiempo.grid(row=1, column=1, padx=5, sticky="w")

        tk.Button(self.root, text="Ingresar Tarea", command=self.gestionar_nueva_tarea).pack(pady=5)
        
        # Separador
        ttk.Separator(self.root, orient='horizontal').pack(fill='x', pady=10)

        # Marco para el estado del procesador
        self.lbl_estado_proc = tk.Label(self.root, text="Procesador: Libre", fg="green", font=("Arial", 10, "bold"))
        self.lbl_estado_proc.pack(pady=5)

        self.lbl_conteo = tk.Label(self.root, text="", font=("Arial", 10))
        self.lbl_conteo.pack()

        # Marco para la Pila (Columna)
        tk.Label(self.root, text="Pila de Tareas (Cima arriba):").pack(pady=5)
        
        # Se usa un Listbox para representar la columna. 
        self.listbox_pila = tk.Listbox(self.root, height=10, width=40, justify="center")
        self.listbox_pila.pack(pady=5)

    def gestionar_nueva_tarea(self):
        tipo = self.combo_tipo.get()
        try:
            # Caso límite corregido: Forzar a entero para que el conteo inverso tenga sentido
            tiempo = int(self.entrada_tiempo.get())
            if tiempo <= 0: raise ValueError
        except ValueError:
            messagebox.showerror("Error de Lógica", "El tiempo debe ser un número entero positivo mayor a cero.")
            return

        nueva_tarea = Tarea(tipo, tiempo)

        if not self.procesador_ocupado:
            self.ejecutar_tarea_hilo(nueva_tarea)
        else:
            self.pila.apilar(nueva_tarea)
            self.actualizar_interfaz_pila()
            
        self.entrada_tiempo.delete(0, tk.END)

    def ejecutar_tarea_hilo(self, tarea):
        hilo = threading.Thread(target=self.rutina_procesador, args=(tarea,), daemon=True)
        hilo.start()

    def rutina_procesador(self, tarea_inicial):
        self.procesador_ocupado = True
        tarea_actual = tarea_inicial

        while tarea_actual is not None:
            self.lbl_estado_proc.config(text=f"Procesador: Ejecutando {tarea_actual.tipo}", fg="red")
            
            # Lógica de conteo regresivo
            tiempo_restante = tarea_actual.tiempo
            while tiempo_restante > 0:
                self.lbl_conteo.config(text=f"Tiempo restante: {tiempo_restante}s")
                time.sleep(1) # Pausa el hilo, no la interfaz
                tiempo_restante -= 1
            
            self.lbl_conteo.config(text="") # Limpia el conteo al terminar
            
            # Desapilar la siguiente tarea
            tarea_actual = self.pila.desapilar()
            self.actualizar_interfaz_pila()

        # Liberar procesador
        self.procesador_ocupado = False
        self.lbl_estado_proc.config(text="Procesador: Libre", fg="green")
        self.lbl_conteo.config(text="")

    def actualizar_interfaz_pila(self):
        # Limpiamos el listbox visual
        self.listbox_pila.delete(0, tk.END)
        
        # Para que se comporte visualmente como una pila, el último en entrar (cima) debe verse arriba.
        # reversed() itera la lista desde el último elemento (índice -1) hasta el primero (índice 0).
        for tipo in reversed(self.pila.obtener_tipos()):
            self.listbox_pila.insert(tk.END, f"[{tipo}]")

if __name__ == "__main__":
    # Solo para pruebas individuales de este script
    root = tk.Tk()
    app = AppRobot(root)
    root.mainloop()