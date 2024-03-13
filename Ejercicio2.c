#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <semaphore.h>
#include <unistd.h>

#define NUM_FILOSOFOS 5

pthread_mutex_t tenedores[NUM_FILOSOFOS];
sem_t mutex;

void *filosofo(void *arg) {
    int id = *(int*)arg;
    int izquierda = id;
    int derecha = (id + 1) % NUM_FILOSOFOS;

    while (1) {
        printf("Filósofo %d pensando...\n", id);
        usleep(rand() % 3000000); // Tiempo pensando

        // Solicitar los tenedores
        sem_wait(&mutex);
        pthread_mutex_lock(&tenedores[izquierda]);
        pthread_mutex_lock(&tenedores[derecha]);
        sem_post(&mutex);

        printf("Filósofo %d comiendo...\n", id);
        usleep(rand() % 3000000); // Tiempo comiendo

        // Liberar los tenedores
        pthread_mutex_unlock(&tenedores[izquierda]);
        pthread_mutex_unlock(&tenedores[derecha]);
    }
}

int main() {
    pthread_t filosofos[NUM_FILOSOFOS];
    int ids[NUM_FILOSOFOS];

    // Inicializar semáforo
    sem_init(&mutex, 0, 1);

    // Inicializar mutex para los tenedores
    for (int i = 0; i < NUM_FILOSOFOS; i++) {
        pthread_mutex_init(&tenedores[i], NULL);
    }

    // Crear hilos para los filósofos
    for (int i = 0; i < NUM_FILOSOFOS; i++) {
        ids[i] = i;
        pthread_create(&filosofos[i], NULL, filosofo, &ids[i]);
    }

    // Esperar a que terminen los hilos
    for (int i = 0; i < NUM_FILOSOFOS; i++) {
        pthread_join(filosofos[i], NULL);
    }

    // Destruir mutex y semáforo
    sem_destroy(&mutex);
    for (int i = 0; i < NUM_FILOSOFOS; i++) {
        pthread_mutex_destroy(&tenedores[i]);
    }

    return 0;
}
