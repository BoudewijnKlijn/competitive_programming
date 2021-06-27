#include <stdio.h>
#include <stdlib.h>

int main()
{
    int i,run,leftover;
    int fibo1[1001] = {0}, fibo2[1001] = {0}, fibo3[1001] = {0};

    fibo1[1000] = 1;
    fibo2[1000] = 1;
    run = 2;

    while(fibo2[1] < 1){
        leftover = 0;
        for (i=1000;i>=0;i--){
            fibo3[i] = leftover + fibo1[i] + fibo2[i];
            leftover = fibo3[i]/10;
            fibo3[i] = fibo3[i]%10;

            fibo1[i] = fibo2[i];
            fibo2[i] = fibo3[i];
        }
        run++;
    }
    printf("%d",run);
    return 0;
}
