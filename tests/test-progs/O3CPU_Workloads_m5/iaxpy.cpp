#include <cstdio>
#include <stdlib.h>
#include <random>
#include "gem5/m5ops.h"

int main()
{
    const int N = 4096;
	int X[N], Y[N], alpha = 2;
	      
	for (int i = 0; i < N; ++i)
	{
	    X[i] = rand() % 2 + 1;
	    Y[i] = rand() % 2 + 1;
	}

	// Start of iaxpy loop
	m5_dump_reset_stats(0, 0);
	for (int i = 0; i < N; ++i)
	{
	    Y[i] = alpha * X[i] + Y[i];
	}
	// End of iaxpy loop
	m5_dump_reset_stats(0, 0);

  	int sum = 0;
  	for (int i = 0; i < N; ++i)
	{
		sum += Y[i];
	}
	printf("%d\n", sum);
	return 0;
}
