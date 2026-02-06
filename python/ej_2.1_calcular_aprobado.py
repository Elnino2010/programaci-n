# Calcula la media de 3 asignaturas
matematicas = float(input("Di tu nota de matemáticas: "))
lengua = float(input("Di tu nota de lengua: "))
historia = float(input("Di tu nota de historia: "))

# Tu código aquí:
print("Vamos a calcular la media de las asignaturas:")
print("matemáticas: ", matematicas)
print("lengua: ", lengua)
print("historia: ", historia)

# 1. Suma las 3 calificaciones
total = matematicas + lengua + historia

# 2. Divide entre 3
media = total / 3

# 3. Imprime el resultado con print()
print(f"La media es {media}") #Usamos media:.2f para que solo muestre 2 decimales ej media

# Añade a tu calculadora:
print("vamos a calcular tu media:")

# - Si la media es >= 5, escribe "Aprobado"
if media >= 5 and media < 9:
    print(f"Tu media es {media:.2f}, por lo que has aprobado")

# - Si no, escribe "Suspenso"
elif media < 5:
    print(f"Tu media es {media:.2f}, por lo que has suspendido")

# - Si es >= 9, añade "¡Excelente!"
elif media >= 9:
    print(f"Tu media es {media:.2f}, por lo que has aprobado y has tenido un desempeño excelente")