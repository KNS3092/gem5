#include <iostream>
#include <pthread.h>
#include <atomic>

#define NUM_THREADS 4
#define ITERS_PER_THREAD 1000000

volatile int counter = 0;

void* increment(void* arg) {
    for (int i = 0; i < ITERS_PER_THREAD; ++i) {
        __sync_fetch_and_add(&counter, 1);  // commutative update
    }
    return nullptr;
}

int main() {
    pthread_t threads[NUM_THREADS];

    for (int i = 0; i < NUM_THREADS; ++i) {
        pthread_create(&threads[i], nullptr, increment, nullptr);
    }

    for (int i = 0; i < NUM_THREADS; ++i) {
        pthread_join(threads[i], nullptr);
    }

    std::cout << "Final counter = " << counter << std::endl;
    return 0;
}

