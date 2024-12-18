/*  Random Branches
    Program to randomly take or not take a branch
*/
#include <stdio.h>
#include <cstdlib>
#include <random>
#include "gem5/m5ops.h"


int main()
{
    const int N = 4096;
    int X[N]; 
    int taken = 0;
    int not_taken = 0;
    for (int i = 0; i < N; ++i)
    {
        X[i] = rand() % 2;
    }

    // Start of Random Branch Loop
    m5_dump_reset_stats(0, 0);
    for (int i = 0; i < N; ++i)
    {
        if (X[i]) {
            taken++;
        } else {
            not_taken++;
        }
    }
    m5_dump_reset_stats(0, 0);
    // End of Random Branch Loop

    printf("# taken: %d, # not taken: %d", taken, not_taken);
    return 0;
}
