#include <cstdio>
#include <stdlib.h>
#include <iostream>

int main()
{
    const int N = 4096;
    double X[N], Y[N], alpha = 0.5;
    
    // Initialize random seed
    srand(42);
    
    // Initialize arrays with random values between 1.0 and 2.0
    for (int i = 0; i < N; ++i)
    {
        X[i] = 1.0 + (double)rand() / RAND_MAX;
        Y[i] = 1.0 + (double)rand() / RAND_MAX;
    }

    // Start of daxpy loop
    for (int i = 0; i < N; ++i)
    {
        Y[i] = alpha * X[i] + Y[i];
    }
    // End of daxpy loop

    double sum = 0;
    for (int i = 0; i < N; ++i)
    {
        sum += Y[i];
    }
    printf("%lf\n", sum);
    return 0;
}
