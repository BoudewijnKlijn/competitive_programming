#include <stdio.h>
#include <stdlib.h>

int main()
{
    int i,j,n,som;
    n = 400;
    int array[n];

    for(i=0;i<sizeof(array)/sizeof(int);i++){
        array[i] = 0;
    }
    array[n-1] = 2;

    for (i=2;i<=1000;i++){
        for(j=0;j<n;j++){
            array[j] *= 2;
            if(array[j]>9){
                array[j] %= 10;
                array[j-1]++;
            }
        }
    }

    som = 0;
    for(i=0;i<sizeof(array)/sizeof(int);i++){
        som += array[i];
    }
    printf("%d",som);
    return 0;
}
