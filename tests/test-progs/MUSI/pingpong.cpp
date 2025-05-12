#include <iostream>
#include <pthread.h>

#define NUM_ITERATIONS 1000000

volatile int shared_var = 0;

void* thread_func1(void* arg) {
    for (int i = 0; i < NUM_ITERATIONS; ++i) {
        __sync_synchronize();  // Memory barrier
        shared_var = 1;
    }
    return nullptr;
}

void* thread_func2(void* arg) {
    for (int i = 0; i < NUM_ITERATIONS; ++i) {
        __sync_synchronize();  // Memory barrier
        shared_var = 2;
    }
    return nullptr;
}

int main() {
    pthread_t t1, t2;

    pthread_create(&t1, nullptr, thread_func1, nullptr);
    pthread_create(&t2, nullptr, thread_func2, nullptr);

    pthread_join(t1, nullptr);
    pthread_join(t2, nullptr);

    std::cout << "Final value: " << shared_var << std::endl;
    return 0;
}
