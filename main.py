import tkinter as tk
from impresora_cola import AppImpresora
from robot_pila import AppRobot

def abrir_impresora():
    ventana_impresora = tk.Toplevel(root)
    AppImpresora(ventana_impresora)

def abrir_robot():
    ventana_robot = tk.Toplevel(root)
    AppRobot(ventana_robot)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Menú Principal - Laboratorio 3")
    root.geometry("300x150")

    tk.Label(root, text="Seleccione el simulador a ejecutar", font=("Arial", 12)).pack(pady=10)
    tk.Button(root, text="Ejercicio 7.1: Cola de Impresión", command=abrir_impresora).pack(fill=tk.X, padx=20, pady=5)
    tk.Button(root, text="Ejercicio 7.2: Pila del Robot", command=abrir_robot).pack(fill=tk.X, padx=20, pady=5)

    root.mainloop()