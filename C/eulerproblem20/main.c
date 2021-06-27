#include <stdio.h>
#include <stdlib.h>

int main()
{
    int i,j,number,leftover,som;
    int array[160] = {0};
    array[sizeof(array)/sizeof(int)-1] = 1;

    number = 0;
    for(i=2;i<=100;i++){
        leftover = 0;
        for(j=sizeof(array)/sizeof(int)-1;j>=0;j--){
            number = leftover + i*array[j];
            array[j] = number%10;
            leftover = number/10;
        }
    }

    som = 0;
    for(i=0;i<sizeof(array)/sizeof(int);i++){
        som += array[i];
    }

    printf("\n\nanswer: %d", som);

    return 0;
}
