import threading
import time

# se crean los recursos compartidos
recurso1 = threading.Lock()
recurso2 = threading.Lock()

# funcion para el primer proceso
def proceso1():
    print("Proceso 1 iniciado")
    while True:
        print("Proceso 1 intentando adquirir recurso 1")
        recurso1.acquire()
        print("Proceso 1 adquirió recurso 1")
        time.sleep(1)
        print("Proceso 1 intentando adquirir recurso 2")
        recurso2.acquire()
        print("Proceso 1 adquirió recurso 2")
        # Simulamos el uso de los recursos
        time.sleep(1)
        # Liberamos los recursos
        recurso2.release()
        recurso1.release()

# funcion para el segundo proceso
def proceso2():
    print("Proceso 2 iniciado")
    while True:
        print("Proceso 2 intentando adquirir recurso 2")
        recurso2.acquire()
        print("Proceso 2 adquirió recurso 2")
        time.sleep(1)
        print("Proceso 2 intentando adquirir recurso 1")
        recurso1.acquire()
        print("Proceso 2 adquirió recurso 1")
        # Simulamos el uso de los recursos
        time.sleep(1)
        # Liberamos los recursos
        recurso1.release()
        recurso2.release()

# se crean los hilos para cada proceso
hilo_proceso1 = threading.Thread(target=proceso1)
hilo_proceso2 = threading.Thread(target=proceso2)

# Inician los hilos
hilo_proceso1.start()
hilo_proceso2.start()

# Esperamos a que los hilos terminen (Nunca va a pasar)
hilo_proceso1.join()
hilo_proceso2.join()
