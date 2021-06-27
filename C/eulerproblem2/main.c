#include <stdio.h>
#include <stdlib.h>

int main()
{
    int fibo1,fibo2,fibo3,som,max_value;
    fibo1 = 1;
    fibo2 = 2;
    fibo3 = fibo1 + fibo2;
    som = fibo2;
    max_value = 4000000;

    while (fibo3 < max_value){
        fibo3 = fibo1 + fibo2;
        fibo1 = fibo2;
        fibo2 = fibo3;
        if (fibo3%2 == 0 && fibo3 < max_value){
            som += fibo3;
        }
    }
    return som;
}
