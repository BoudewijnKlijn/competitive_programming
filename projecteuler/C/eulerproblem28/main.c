#include <stdio.h>
#include <stdlib.h>

int main()
{
    int i,j;
    int x = 1;
    long long sum = 1;
    int side = 1001; /*odd number: 1,3,5 etc*/

    for (i=1;i<=side/2;i++){
        for(j=1;j<=4;j++){
            x += 2*i;
            sum += x;
        }
    }

    printf("answer: %lld",sum);
    return 0;
}
