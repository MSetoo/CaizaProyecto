import tkinter as tk
from tkinter import simpledialog, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

def graficar_barra_y_nodos(puntos_apoyo):
    fig, ax = plt.subplots(figsize=(6, 4))

    # Dibujar la barra horizontal
    ax.plot([1, puntos_apoyo], [0, 0], color='brown', linewidth=5, zorder=1)

    # Dibujar nodos y líneas verticales (puntos de apoyo)
    for i in range(puntos_apoyo):
        x_pos = i + 1
        ax.plot([x_pos, x_pos], [-0.2, 0.2], color='black', linewidth=3, zorder=2)  # Línea vertical
        ax.plot(x_pos, 0.2, 'ro', zorder=3)  # Nodo superior
        ax.text(x_pos, 0.25, f'Nodo {2*i+1}', color='red', fontsize=10, ha='center')
        ax.plot(x_pos, -0.2, 'ro', zorder=3)  # Nodo inferior
        ax.text(x_pos, -0.3, f'Nodo {2*i+2}', color='red', fontsize=10, ha='center')

    # Configuración del gráfico
    ax.set_title("Barra y Nodos", fontsize=14)
    ax.set_xlim(0.5, puntos_apoyo + 0.5)
    ax.set_ylim(-0.5, 0.5)
    ax.axis('off')  # Ocultar ejes

    return fig

def pedir_matriz(root, tramo, indices_nodos):
    matriz = []
    for i in range(4):
        fila = []
        for j in range(4):
            while True:
                try:
                    valor = simpledialog.askinteger(
                        "Ingreso de matriz",
                        f"Ingrese el valor para la posición ({indices_nodos[i]},{indices_nodos[j]}) del tramo {tramo}:",
                        parent=root,
                    )
                    if valor is not None:
                        fila.append(valor)
                        break
                    else:
                        raise ValueError("Entrada cancelada.")
                except ValueError:
                    messagebox.showerror("Error", "Por favor, ingrese un número entero válido.", parent=root)
        matriz.append(fila)
    return matriz

def mostrar_interfaz():
    def cerrar_ventana():
        root.destroy()

    def pedir_puntos_apoyo():
        while True:
            try:
                puntos = simpledialog.askinteger("Puntos de Apoyo", "Ingrese el número de puntos de apoyo:", parent=root, minvalue=1)
                if puntos is not None:
                    return puntos
                else:
                    tk.messagebox.showinfo("Cancelado", "Operación cancelada. Cerrando el programa.")
                    root.destroy()
                    return None
            except ValueError:
                tk.messagebox.showerror("Error", "Por favor, ingrese un número válido.")

    # Crear ventana principal
    root = tk.Tk()
    root.title("Sistema de Matrices")
    root.geometry("800x600")
    root.configure(bg='lightblue')

    # Pedir el número de puntos de apoyo
    puntos_apoyo = pedir_puntos_apoyo()
    if puntos_apoyo is None:
        return  # Si el usuario cancela, se cierra la aplicación

    # Crear el gráfico
    fig = graficar_barra_y_nodos(puntos_apoyo)
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(pady=20)

    # Crear matriz para cada tramo
    tramos = puntos_apoyo - 1  # El número de tramos es uno menos que el número de puntos de apoyo
    matriz_global = []
    indice_inicio = 1  # Comienza en 1 para el primer tramo

    for tramo in range(1, tramos + 1):
        # Definir los índices para el tramo actual
        indices_nodos = list(range(indice_inicio, indice_inicio + 4))
        messagebox.showinfo("Ingreso de Tramo", f"Ingrese los valores de la matriz para el tramo {tramo}.", parent=root)
        matriz = pedir_matriz(root, tramo, indices_nodos)
        matriz_global.append(matriz)

        # Actualizar el índice de inicio para el siguiente tramo
        indice_inicio += 4

    # Mostrar matrices ingresadas con formato
    mensaje = "Matrices Ingresadas:\n\n"
    for idx, matriz in enumerate(matriz_global, start=1):
        mensaje += f"Tramo {idx}:\n"
        # Formatear la matriz con un espaciado uniforme
        for fila in matriz:
            mensaje += "  ".join([f"{elem:4d}" for elem in fila]) + "\n"
        mensaje += "\n"
    
    messagebox.showinfo("Matrices Globales", mensaje, parent=root)

    # Botón para salir
    boton_salir = tk.Button(root, text="Salir", command=cerrar_ventana, bg="red", fg="white", font=("Arial", 12, "bold"))
    boton_salir.pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    mostrar_interfaz()
