# Crea una lista con 5 asignaturas
asignaturas = ["Matemáticas", "Lengua", "Historia", "Física", "Química"]
notas = []

# Usa un bucle for para pedir la nota de cada asignatura
for i in range(len(asignaturas)):
    notas.append(float(input(f"Di tu nota de {asignaturas[i]}: ")))
# Almacénalas en otra lista llamada 'notas'