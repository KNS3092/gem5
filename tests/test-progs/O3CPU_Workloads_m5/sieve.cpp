#include<iostream>
#include<string.h>
#include<stdlib.h>
#include "gem5/m5ops.h"
using namespace std;

int primeCount(int n)
{
    int count=0;
    bool isPrime[n+1];
    memset(isPrime,1,sizeof(isPrime));
    
    //Sieve of Eratosthenes implementation
    if(n<2)
    {
        return 0;
    }
    else
    {
        for(int i=2; i*i<=n; i++)
        {
            if(isPrime[i]==1)
            {
                for (int j=i*i;j<=n;j+=i)
                isPrime[j]=0;
            }
        }

        //Counting the number of primes
        for(int c=2;c<=n;c++)
        {
            if(isPrime[c]==1)
            {
                count++;
            }
        }
        return count;
    }
}

int main()
{

    int num= 4096;
    m5_dump_reset_stats(0, 0);
    cout<<primeCount(num)<<endl;
    m5_dump_reset_stats(0, 0);

    return 0;
}
