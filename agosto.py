fecha = input("Di una fecha (dd/mm/yyyy): ")
bar = 0
d = []
m = []
print(fecha)
for i in fecha:
    if i == "0":
        d.append(0)
    if i == "1":
        d.append(1)
    if i == "2":
        d.append(2)
    if i == "3":
        d.append(3)
    if i == "4":
        d.append(4)
    if i == "5":
        d.append(5)
    if i == "6":
        d.append(6)
    if i == "7":
        d.append(7)
    if i == "8":
        d.append(8)
    if i == "9":
        d.append(9)
    if i == "/":
        d.append("/")
for n in d:
    if n == "/":
        bar += 1
    elif bar == 1:
        m.append(n)
m[0] == m[0]*10
bar == sum(m)
if bar == 8:
    print("Es agosto")
else:
    print("No es agosto")

    