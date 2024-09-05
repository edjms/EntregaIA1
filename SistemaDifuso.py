import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
import skfuzzy as fuzz
import skfuzzy.control as ctrl
import numpy as np

# Definir el universo de valores
clima_universe = np.arange(0, 1.1, 0.1)
velocidad_universe = np.arange(0, 201, 1)
velocidad_recomendada_universe = np.arange(0, 101, 1)

# Crear las variables de entrada y salida
clima = ctrl.Antecedent(clima_universe, 'clima')
velocidad_actual = ctrl.Antecedent(velocidad_universe, 'velocidad_actual')
velocidad_recomendada = ctrl.Consequent(velocidad_recomendada_universe, 'velocidad_recomendada')

# Definir los conjuntos difusos usando trapmf y trimf
clima['sin_lluvia'] = fuzz.trapmf(clima_universe, [0, 0, 0.5, 1])
clima['con_lluvia'] = fuzz.trapmf(clima_universe, [0, 0.5, 1, 1])

velocidad_actual['baja'] = fuzz.trimf(velocidad_universe, [0, 0, 100])
velocidad_actual['media'] = fuzz.trimf(velocidad_universe, [0, 100, 200])
velocidad_actual['alta'] = fuzz.trimf(velocidad_universe, [100, 200, 200])

velocidad_recomendada['baja'] = fuzz.trimf(velocidad_recomendada_universe, [0, 0, 50])
velocidad_recomendada['media'] = fuzz.trimf(velocidad_recomendada_universe, [0, 50, 100])
velocidad_recomendada['alta'] = fuzz.trimf(velocidad_recomendada_universe, [50, 100, 100])

# Definir las reglas
regla1 = ctrl.Rule(clima['sin_lluvia'] & velocidad_actual['baja'], velocidad_recomendada['media'])
regla2 = ctrl.Rule(clima['sin_lluvia'] & velocidad_actual['media'], velocidad_recomendada['alta'])
regla3 = ctrl.Rule(clima['con_lluvia'] & velocidad_actual['baja'], velocidad_recomendada['baja'])
regla4 = ctrl.Rule(clima['con_lluvia'] & velocidad_actual['media'], velocidad_recomendada['media'])

# Crear el sistema de control
sistema_control = ctrl.ControlSystem([regla1, regla2, regla3, regla4])
sistema_simulacion = ctrl.ControlSystemSimulation(sistema_control)

def mostrar_grafica():
    try:
        clima_input = float(entry_clima.get())
        velocidad_input = float(entry_velocidad.get())

        sistema_simulacion.input['clima'] = clima_input
        sistema_simulacion.input['velocidad_actual'] = velocidad_input
        sistema_simulacion.compute()

        velocidad_resultado = sistema_simulacion.output['velocidad_recomendada']
        label_resultado.config(text=f"Velocidad recomendada: {velocidad_resultado:.2f} km/h")

        # Graficar resultados
        clima.view(sim=sistema_simulacion)
        velocidad_actual.view(sim=sistema_simulacion)
        velocidad_recomendada.view(sim=sistema_simulacion)
        plt.show()

    except ValueError:
        messagebox.showerror("Error", "Por favor, ingresa números válidos.")
    except Exception as e:
        messagebox.showerror("Error", f"Ha ocurrido un error: {str(e)}")

# Crear la ventana principal
root = tk.Tk()
root.title("Control Difuso de Velocidad de Motocicleta")

tk.Label(root, text="Condiciones climáticas (0: Sin lluvia, 1: Con lluvia):").grid(row=0, column=0)
entry_clima = tk.Entry(root)
entry_clima.grid(row=0, column=1)

tk.Label(root, text="Velocidad actual (km/h):").grid(row=1, column=0)
entry_velocidad = tk.Entry(root)
entry_velocidad.grid(row=1, column=1)

boton_calcular = tk.Button(root, text="Calcular Velocidad", command=mostrar_grafica)
boton_calcular.grid(row=2, column=0, columnspan=2)

label_resultado = tk.Label(root, text="Velocidad recomendada:")
label_resultado.grid(row=3, column=0, columnspan=2)

# Botón para mostrar la gráfica
boton_grafica = tk.Button(root, text="Mostrar Gráfica", command=mostrar_grafica)
boton_grafica.grid(row=4, column=0, columnspan=2)

root.mainloop()
