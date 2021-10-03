#include <stdio.h>
#include <stdlib.h>

int n_divisors(long long number){
    int i, n;

    n = 0;

    for (i=1;i*i<=number;i++){
        if(number%i==0){
            if(i*i<number){
               n += 2;
            }
            else{
                n += 1;
            }
        }
    }
    return n;
}

int main()
{
    int i;
    long long number;

    i = 1;
    number = i;

    while (n_divisors(number) < 500){
        i++;
        number += i;
    }

    printf("%d",number);
    return 0;
}
