#include <stdio.h>
#include <stdlib.h>

int is_equal(long long number, int *array){
    long long number_original = number, sum = 0;
    while(number>0){
        sum += array[number%10];
        number /= 10;
    }
    if(sum==number_original){
        return 1;
    }
    else{
        return 0;
    }
}

int main()
{
    int array[10], i, j, sum = 0;
    array[0] = 1;
    for(i=1;i<10;i++){
        array[i] = array[i-1]*i;
    }

    for(j=10;j<10000000;j++){ /* 9.999.999 > 7*9!, dus vandaar deze boven limiet */
        if(is_equal(j,array)){
            sum += j;
        }
    }
    printf("answer: %d",sum);
    return 0;
}
