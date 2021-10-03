#include <stdio.h>
#include <stdlib.h>

int main()
{
    long long number, i, n, largest, largest_index;
    long long *chain_length;

    chain_length = malloc(999999 * sizeof(long long));
    if (chain_length==NULL){
        printf("error");
        return 1;
    }

    largest = 1;
    largest_index = 0;
    chain_length[0] = 1;

    for (i=2;i<=999999;i++){
        n = 0;
        number = i;
        while (number != 1 && number > i-1 ){
            n++;
            if(number%2==0){
                number /= 2;
            }
            else{
                number = 3*number + 1;
            }
        }
        if (number<i){
            n += chain_length[number-1];
        }
        chain_length[i-1] = n;
        if (n>largest){
            largest = n;
            largest_index = i-1;
        }
    }

    printf("%d",largest_index+1);
    return 0;
}
