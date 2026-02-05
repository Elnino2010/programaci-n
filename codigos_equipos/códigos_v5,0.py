'''
Fecha: 14-11-25
Programa: 5 6 7
Equipo: robot city pobra
Definitivo: No
'''
#______________________LIBRERIAS_A_IMPORTAR___________________________ 
# 
from pybricks.hubs import PrimeHub 
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor, ForceSensor  #Son los elementos del robot que interactúan con el entorno
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop 
from pybricks.robotics import DriveBase 
from pybricks.tools import wait, StopWatch

#definir hub 
hub = PrimeHub()

#definir las ruedas 
rueda_izquierda = Motor(Port.A, Direction.COUNTERCLOCKWISE) 
rueda_derecha = Motor(Port.B, Direction.CLOCKWISE) 
motor_derecha =Motor(Port.F)  
motor_izquierda =Motor(Port.E)
sensor_dcha =ColorSensor(Port.C)
sensor_izda =ColorSensor(Port.D)

#Configurar drive base (rueda_izquierda, rueda_derecha, diámetro_ruedas, distancia_ejes) 
robot = DriveBase(rueda_izquierda, rueda_derecha, 54, 128) 

#robot.settings(velocidad, aceleraciones, velocidad giros, aceleración giros) 
robot.settings(500,300,50,30)

#Esta función se usa para mover el robot en linea recta durante una distancia y velocidad
def recorrer(distancia, velocidad, aceleracion = True): #(distancia en mm siempre en positivo, velocidad desde -1100 a 1000)
    direccion = 1 if distancia >= 0 else -1 
    velocidad_ajustada = abs(velocidad) * direccion 
    distancia_absoluta = abs(distancia) 
    angulo_inicial = hub.imu.heading() 
    kp = 1
    robot.reset() 

    velocidad_abs = abs(velocidad)
    
    # Zona de desaceleración proporcional a la velocidad
    if velocidad_abs <= 150:
        distancia_frenado = 80  
    elif velocidad_abs <= 300:
        distancia_frenado = 150
    else:
        # Para velocidades muy altas, zona de frenado mucho mayor
        distancia_frenado = velocidad_abs * 0.6
    #Aquí el robot empieza a avanzar en linea recta
    while abs(robot.distance()) < distancia_absoluta: 
        distancia_recorrida = abs(robot.distance())
        distancia_restante = distancia_absoluta - distancia_recorrida
        
        # Desaceleración progresiva
        if aceleracion and distancia_restante < distancia_frenado:
            factor_velocidad = distancia_restante / distancia_frenado
            factor_velocidad = max(0.1, factor_velocidad)
            velocidad_actual = velocidad_ajustada * factor_velocidad
        #Calcular el error del desvío al avanzar
        else:
            velocidad_actual = velocidad_ajustada
        angulo_actual = hub.imu.heading()
        error = angulo_inicial - angulo_actual
        correccion = error * kp
        
        robot.drive(velocidad_actual, correccion) 
        wait(10) 
    for i in range(5):
        hub.imu.heading()  # Leer varias veces para estabilizar
        wait(20)
    
    robot.stop()
    wait(500)

def recorrer_tiempo(tiempo_ms, velocidad=100, desacelerar=True):# Aquí en vez de usar distancia en mm usamos tiempo en ms, la velocidad y aceleración queda igual

    # Esperar estabilización inicial
    wait(50)
    
    direccion = 1 if velocidad >= 0 else -1
    velocidad_abs = abs(velocidad)
    
    # Leer ángulo varias veces para asegurar estabilidad
    angulo_inicial = 0
    for i in range(3):
        angulo_inicial = hub.imu.heading()
        wait(10)
    
    kp = 1  # Control suave
    
    # Zona de desaceleración proporcional a la velocidad
    if velocidad_abs <= 150:
        tiempo_frenado = 300  # 300 ms
    elif velocidad_abs <= 300:
        tiempo_frenado = 500  # 500 ms
    else:
        tiempo_frenado = velocidad_abs * 2  # A más velocidad, más tiempo de frenado
    
    # Crear cronómetro
    cronometro = StopWatch()
    
    while cronometro.time() < tiempo_ms:
        # Calcular tiempo transcurrido y restante
        tiempo_transcurrido = cronometro.time()
        tiempo_restante = tiempo_ms - tiempo_transcurrido
        
        # Aplicar desaceleración si está activada
        if desacelerar and tiempo_restante < tiempo_frenado:
            factor_velocidad = tiempo_restante / tiempo_frenado
            factor_velocidad = max(0.1, factor_velocidad)  # Velocidad mínima 10%
            velocidad_actual = velocidad * factor_velocidad
        else:
            velocidad_actual = velocidad
        
        # Control de dirección con girosensor
        angulo_actual = hub.imu.heading()
        error = angulo_inicial - angulo_actual
        correccion = error * kp
        
        # Limitar corrección
        correccion = max(-40, min(40, correccion))
        
        robot.drive(velocidad_actual, correccion)
        wait(10)
    
    for i in range(5):
        hub.imu.heading()  # Leer varias veces para estabilizar
        wait(20)

    robot.stop()
    wait(500)  # Pausa para estabilización

def giro_mismo(angulo_grados, velocidad_giro=90):#negativos izquierda, positivos derecha 
    angulo_inicial = hub.imu.heading() #Usamos el girosensor del robot
    angulo_objetivo = angulo_inicial + angulo_grados
    if angulo_objetivo > 180:
        angulo_objetivo -= 360
    elif angulo_objetivo < -180:
        angulo_objetivo += 360
    direccion = 1 if angulo_grados >= 0 else -1 
    velocidad_ajustada = abs(velocidad_giro) * direccion 
    factor_correccion = 1.0
    factor_minimo = 0.3

    while True:
      #calculamos el error con un margen de un grado
        angulo_actual = hub.imu.heading() 
        error = angulo_objetivo - angulo_actual 
        if error > 180:
            error -= 360 
        elif error < -180: 
            error += 360
        if abs(error) < 1: 
            break
        factor_prop = abs(error) / 90
        if factor_prop < factor_minimo:
            factor_prop = factor_minimo
        if factor_prop > 1:
            factor_prop = 1
        velocidad_actual = velocidad_ajustada * factor_prop
        if (error * direccion) < 0:
            velocidad_actual = -velocidad_actual
        #gira teniendo en cuenta el ángulo y la velocidad
        robot.drive(0, velocidad_actual)
        wait(10)
    robot.stop()
    wait(500)
    
def giro_punto(velocidad_avance, angulo_grados, velocidad_giro=90): #gira mientras avanza
    #Primero coje el ángulo y la dirección del giro
    angulo_inicial = hub.imu.heading()
    angulo_objetivo = angulo_inicial + angulo_grados 
    if angulo_objetivo > 180: 
        angulo_objetivo -= 360 
    elif angulo_objetivo < -180: 
        angulo_objetivo += 360 
    direccion = 1 if angulo_grados >= 0 else -1 
    velocidad_ajustada = abs(velocidad_giro) * direccion 
    factor_minimo = 0.3 
    while True:
        #calcula el error en el giro
        angulo_actual = hub.imu.heading()
        error = angulo_objetivo - angulo_actual 
        if error > 180: 
            error -= 360 
        elif error < -180: 
            error += 360 
        if abs(error) < 1: 
            break 
        factor_prop = abs(error) / 90 
        if factor_prop < factor_minimo: 
            factor_prop = factor_minimo 
        if factor_prop > 1: 
            factor_prop = 1 
        velocidad_actual = velocidad_ajustada * factor_prop 
        if (error * direccion) < 0: 
            velocidad_actual = -velocidad_actual
        #Ahora el robot gira y avanza al mismo tiempo
        robot.drive(velocidad_avance, velocidad_actual) 
        wait(10)
    robot.stop()
    wait(500)

def avanzar_hasta_linea(VELOCIDAD): 
    # Avanzar hasta encontrar línea negra con ambos sensores 
    rueda_izquierda.run(VELOCIDAD) 
    rueda_derecha.run(VELOCIDAD) 
     
    # leer los sensores
    intensidad_izda = sensor_izda.reflection() 
    intensidad_dcha = sensor_dcha.reflection() 
     
    # Ciclo principal: avanzar hasta que AMBOS sensores encuentren línea negra 
    while not (intensidad_dcha < 10 and intensidad_izda < 10): 
        # Obtener la intensidad de la luz reflejada (0-100) 
        intensidad_izda = sensor_izda.reflection() 
        intensidad_dcha = sensor_dcha.reflection() 
        if intensidad_dcha < 10: 
            rueda_derecha.stop() 
        if intensidad_izda < 10: 
            rueda_izquierda.stop() 
        # Esperar un poco antes de la siguiente lectura 
        wait(10) 
     
    # Detener ambos motores cuando ambos sensores detecten negro 
     
    # Fase 2: Ajustarse con la línea blanca que está detrás 
    # Retroceder ligeramente para posicionarse en la línea blanca 
    rueda_izquierda.run_time(-VELOCIDAD, 200)  # Retroceder un poco 
    rueda_derecha.run_time(-VELOCIDAD, 200) 
    wait(300)  # Esperar a que termine el movimiento 
     
    # Ajuste en la línea blanca 
    ajuste_completado = False 
    intentos_maximos = 50  # Limitar intentos para evitar bucle infinito 
    intentos = 0 
     
    while not ajuste_completado and intentos < intentos_maximos: 
        intensidad_izda = sensor_izda.reflection() 
        intensidad_dcha = sensor_dcha.reflection() 
        print(f"Izda: {intensidad_izda}, Dcha: {intensidad_dcha}") 
         
        # Si un sensor está en negro (menor que 10), ajustar 
        if intensidad_izda < 10: 
            # Sensor izquierdo en negro, mover ligeramente hacia atrás 
            rueda_izquierda.run_time(-200, 100) 
            wait(120) 
        elif intensidad_dcha < 10: 
            # Sensor derecho en negro, mover ligeramente hacia atrás 
            rueda_derecha.run_time(-200, 100) 
            wait(120) 
        elif intensidad_dcha > 50 and intensidad_izda > 50: 
            # Ambos sensores están en zona clara/blanca 
            ajuste_completado = True 
         
        intentos += 1 
        wait(10) 
    # Asegurar que ambos motores estén detenidos 
    rueda_izquierda.stop() 
    rueda_derecha.stop() 
    angulo_inicial = hub.imu.heading() 
    angulo_objetivo = angulo_inicial + angulo_grados 
    if angulo_objetivo > 180: 
        angulo_objetivo -= 360 
    elif angulo_objetivo < -180: 
        angulo_objetivo += 360 
    direccion = 1 if angulo_grados >= 0 else -1 
    velocidad_ajustada = abs(velocidad_giro) * direccion 
    factor_correccion = 1.0 
    factor_minimo = 0.3 
    while True: 
        angulo_actual = hub.imu.heading() 
        error = angulo_objetivo - angulo_actual 
        if error > 180: 
            error -= 360 
        elif error < -180: 
            error += 360 
        if abs(error) < 1: 
            break 
        factor_prop = abs(error) / 90 
        if factor_prop < factor_minimo: 
            factor_prop = factor_minimo 
        if factor_prop > 1: 
            factor_prop = 1 
        velocidad_actual = velocidad_ajustada * factor_prop 
        if (error * direccion) < 0: 
            velocidad_actual = -velocidad_actual 
        robot.drive(0, velocidad_actual) 
        wait(10) 
      
    robot.stop() 
 

programas = 0 

max_programas = 9 

hub.display.number(1) 

while True: 

    if programas == 1: 
        hub.display.icon([ 
        [0, 0, 100, 0, 0], 
        [0, 100, 100, 0, 0], 
        [0, 0, 100, 0, 0], 
        [0, 1, 100, 0, 0], 
        [0, 100, 100, 100, 0] 
        ]) 
        if Button.BLUETOOTH in hub.buttons.pressed(): 
            wait(200) 

    if programas == 2: 

        hub.display.icon([ 
        [0, 100, 100, 100, 0], 
        [0, 0, 0, 100, 0], 
        [0, 100, 100, 100, 0], 
        [0, 100, 0, 0, 0], 
        [0, 100, 100, 100, 0] 
        ]) 

        if Button.BLUETOOTH in hub.buttons.pressed(): 
            print("hola")
            wait(200) 

    if programas == 3: 
        hub.display.icon([ 
        [0, 100, 100, 100, 0], 
        [0, 0, 0, 100, 0], 
        [0, 100, 100, 100, 0], 
        [0, 0, 0, 100, 0], 
        [0, 100, 100, 100, 0] 
        ]) 

        if Button.BLUETOOTH in hub.buttons.pressed(): 
            print("hola") 
            wait(200) 

    if programas == 4: 
        hub.display.icon([ 
        [0, 100, 0, 100, 0], 
        [0, 100, 0, 100, 0], 
        [0, 100, 100, 100, 0], 
        [0, 0, 0, 100, 0], 
        [0, 0, 0, 100, 0] 
        ]) 

        if Button.BLUETOOTH in hub.buttons.pressed(): 
            wait(200) 

    if programas == 5: 
        hub.display.icon([ 
        [0, 100, 100, 100, 0], 
        [0, 100, 0, 0, 0], 
        [0, 100, 100, 100, 0], 
        [0, 0, 0, 100, 0], 
        [0, 100, 100, 100, 0] 
        ])

        if Button.BLUETOOTH in hub.buttons.pressed(): 
            wait(200)

    if programas == 6: 
        hub.display.icon([
        [0, 100, 100, 100, 0],
        [0, 100, 0, 0, 0],
        [0, 100, 100, 100, 0],
        [0, 100, 0, 100, 0],
        [0, 100, 100, 100, 0]
        ]) 

    if programas == 7:
        hub.display.icon([
        [0, 100, 100, 100, 0],
        [0, 0, 0, 100, 0],
        [0, 0, 100, 0, 0],
        [0, 100, 0, 0, 0],
        [0, 100, 0, 0, 0]
        ]) 

        if Button.BLUETOOTH in hub.buttons.pressed(): 
            wait(200)

    if programas == 8:
        hub.display.icon([
        [0, 100, 100, 100, 0],
        [0, 100, 0, 100, 0],
        [0, 100, 100, 100, 0],
        [0, 100, 0, 100, 0],
        [0, 100, 100, 100, 0]
        ]) 

        if Button.BLUETOOTH in hub.buttons.pressed(): 
            wait(200)

    if programas == 9:
        hub.display.icon([
        [0, 100, 100, 100, 0],
        [0, 100, 0, 100, 0],
        [0, 100, 100, 100, 0],
        [0, 0, 0, 100, 0],
        [0, 100, 100, 100, 0]
        ])

        if Button.BLUETOOTH in hub.buttons.pressed(): 
            wait(200)

    if Button.LEFT in hub.buttons.pressed(): 

        if programas == 1: 

            programas = max_programas 

        else: 

            programas -= 1 

        print(programas) 

        wait(200) 

    if Button.RIGHT in hub.buttons.pressed(): 

        if max_programas == programas: 

            programas = 1 

        else:     

            programas += 1 

        print(programas) 

        wait(200) 