class BankerAlgorithm:
    def __init__(self, n_processes, n_resources):
        self.n_processes = n_processes
        self.n_resources = n_resources
        self.max_resources = [5, 3, 7]  # Cantidad máxima de recursos disponibles
        self.available_resources = self.max_resources.copy()

        self.allocation = [[0] * n_resources for _ in range(n_processes)]
        self.max_claim = [[0] * n_resources for _ in range(n_processes)]

        self.initialize_processes()

    def initialize_processes(self):
        # Simulación de asignación máxima para cada proceso
        self.max_claim[0] = [7, 5, 3]
        self.max_claim[1] = [3, 2, 2]
        self.max_claim[2] = [9, 0, 2]
        self.max_claim[3] = [2, 2, 2]
        self.max_claim[4] = [4, 3, 3]

    def request_resources(self, process_id, request):
        # Verificar si la solicitud es válida
        if all(0 <= request[i] <= self.max_claim[process_id][i] for i in range(self.n_resources)):
            # Verificar si hay suficientes recursos disponibles
            if all(request[i] <= self.available_resources[i] for i in range(self.n_resources)):
                # Simular asignación temporal
                for i in range(self.n_resources):
                    self.available_resources[i] -= request[i]
                    self.allocation[process_id][i] += request[i]

                # Verificar si la asignación temporal es segura
                if self.is_safe():
                    return True
                else:
                    # Deshacer la asignación temporal si no es segura
                    for i in range(self.n_resources):
                        self.available_resources[i] += request[i]
                        self.allocation[process_id][i] -= request[i]
                    return False
            else:
                return False
        else:
            return False

    def release_resources(self, process_id, release):
        # Liberar los recursos asignados
        for i in range(self.n_resources):
            self.available_resources[i] += release[i]
            self.allocation[process_id][i] -= release[i]

    def is_safe(self):
        # Verificar si existe una secuencia segura utilizando el algoritmo del banquero
        work = self.available_resources.copy()
        finish = [False] * self.n_processes

        while True:
            # Buscar un proceso que pueda ejecutar de manera segura
            found = False
            for i in range(self.n_processes):
                if not finish[i] and all(self.allocation[i][j] <= work[j] for j in range(self.n_resources)):
                    # Ejecutar el proceso de manera segura
                    for j in range(self.n_resources):
                        work[j] += self.allocation[i][j]
                    finish[i] = True
                    found = True

            # Si no se encuentra ningún proceso seguro, salir del bucle
            if not found:
                break

        # Verificar si todos los procesos se ejecutaron de manera segura
        return all(finish)

# Ejemplo de uso
banker = BankerAlgorithm(n_processes=5, n_resources=3)

# Proceso 1 solicita recursos
if banker.request_resources(process_id=0, request=[3, 2, 2]):
    print("Proceso 1 tiene recursos asignados.")
else:
    print("Proceso 1 no puede obtener los recursos.")

# Proceso 2 solicita recursos
if banker.request_resources(process_id=1, request=[1, 0, 2]):
    print("Proceso 2 tiene recursos asignados.")
else:
    print("Proceso 2 no puede obtener los recursos.")

# Proceso 1 libera recursos
banker.release_resources(process_id=0, release=[1, 1, 1])

# Proceso 3 solicita recursos
if banker.request_resources(process_id=2, request=[4, 2, 2]):
    print("Proceso 3 tiene recursos asignados.")
else:
    print("Proceso 3 no puede obtener los recursos.")
