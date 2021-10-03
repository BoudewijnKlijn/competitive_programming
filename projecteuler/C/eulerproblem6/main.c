#include <stdio.h>
#include <stdlib.h>

int main()
{
    int ssq, sqs, i, max;

    max = 100;
    ssq = 0;
    sqs = (1+max)*(max/2)*(1+max)*(max/2);

    for (i=1;i<=max;i++){
        ssq += i*i;
    }

    printf("verschil is %d", sqs-ssq);

    return 0;
}
