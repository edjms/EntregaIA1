from tkinter import *
from tkinter import ttk
import clips

# Crear entorno del sistema experto
sistemaExperto = clips.Environment()
sistemaExperto.clear()

# Definir las reglas
regla_veggie = """(defrule seleccion_veggie 
    (dieta_veggie) =>
    (assert (opcion patatas_bravas))
    (assert (opcion ensalada))
    (assert (opcion verduras_asadas)))"""

regla_baja_cal = """(defrule seleccion_baja_cal
    (dieta_baja_cal) =>
    (assert (opcion ensalada))
    (assert (opcion verduras_asadas))
    (assert (opcion curry)))"""

regla_picante = """(defrule seleccion_picante
    (dieta_picante) =>
    (assert (opcion patatas_bravas))
    (assert (opcion tacos_picantes))
    (assert (opcion curry)))"""

regla_veggie_baja_cal = """(defrule seleccion_veggie_baja_cal
    (dieta_veggie)
    (dieta_baja_cal) =>
    (assert (opcion ensalada))
    (assert (opcion verduras_asadas)))"""

regla_veggie_pic = """(defrule seleccion_veggie_pic
    (dieta_veggie)
    (dieta_picante) =>
    (assert (opcion curry))
    (assert (opcion patatas_bravas)))"""

regla_picante_baja_cal = """(defrule seleccion_picante_baja_cal
    (dieta_picante)
    (dieta_baja_cal) =>
    (assert (opcion curry)))"""

# Construir reglas en el sistema experto
sistemaExperto.build(regla_veggie)
sistemaExperto.build(regla_baja_cal)
sistemaExperto.build(regla_picante)
sistemaExperto.build(regla_veggie_baja_cal)
sistemaExperto.build(regla_veggie_pic)
sistemaExperto.build(regla_picante_baja_cal)

# Función para ejecutar el sistema experto según las opciones seleccionadas
def ejecutar_sistema_experto():
    # Limpiar hechos anteriores
    sistemaExperto.reset()
    
    # Insertar hechos según las selecciones del usuario
    if veggie_var.get():
        sistemaExperto.assert_string("(dieta_veggie)")
    if baja_cal_var.get():
        sistemaExperto.assert_string("(dieta_baja_cal)")
    if picante_var.get():
        sistemaExperto.assert_string("(dieta_picante)")
    
    # Ejecutar el sistema experto
    sistemaExperto.run()
    
    # Obtener las opciones recomendadas
    recomendaciones = []
    for hecho in sistemaExperto.facts():
        if hecho.template.name == "opcion":
            recomendaciones.append(" ".join(str(hecho)[1:-1].split()[1:]))
    
    # Mostrar las recomendaciones en la interfaz
    resultado_label.config(text="\n".join(recomendaciones))

# Configuración de la interfaz gráfica
root = Tk()
root.title("Selección de Cena")

# Variables de selección
veggie_var = BooleanVar()
baja_cal_var = BooleanVar()
picante_var = BooleanVar()

# Crear los elementos de la interfaz
ttk.Label(root, text="Selecciona tus preferencias de dieta:").grid(column=0, row=0, padx=10, pady=10)

ttk.Checkbutton(root, text="Dieta Vegetariana", variable=veggie_var).grid(column=0, row=1, padx=10, pady=5, sticky=W)
ttk.Checkbutton(root, text="Dieta Baja en Calorías", variable=baja_cal_var).grid(column=0, row=2, padx=10, pady=5, sticky=W)
ttk.Checkbutton(root, text="Dieta Picante", variable=picante_var).grid(column=0, row=3, padx=10, pady=5, sticky=W)

ttk.Button(root, text="Mostrar Opciones", command=ejecutar_sistema_experto).grid(column=0, row=4, padx=10, pady=10)

resultado_label = ttk.Label(root, text="", wraplength=200)
resultado_label.grid(column=0, row=5, padx=10, pady=10)

# Ejecutar la interfaz
root.mainloop()
