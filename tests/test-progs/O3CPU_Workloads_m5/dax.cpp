#include <cstdio>
#include <stdlib.h>
#include <random>
#include "gem5/m5ops.h"

int main()
{
	const int N = 4096;
	double X[N], Y[N], alpha = 0.5;
	std::random_device rd; std::mt19937 gen(rd());
	std::uniform_real_distribution<> dis(1, 2);
	for (int i = 0; i < N; ++i)
	{
	    X[i] = dis(gen);
	}

	// Start of dax loop
	m5_dump_reset_stats(0, 0);
	for (int i = 0; i < N; ++i)
	{
		Y[i] = alpha * X[i];
	}
	// End of dax loop
	m5_dump_reset_stats(0, 0);

  	double sum = 0;
  	for (int i = 0; i < N; ++i)
	{
		sum += Y[i];
	}
	printf("%lf\n", sum);
	return 0;
}
