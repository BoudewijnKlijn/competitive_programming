#include <stdio.h>
#include <stdlib.h>

int main()
{
    int i,j,k,l,temp;
    int matrix[10];

    for(i=0;i<10;i++){
        matrix[i] = i;
    }

    for (j=2;j<=1000000;j++){
        k = 8;
        l = 9;
        while(matrix[k]>matrix[k+1]){
            k--;
        }
        while(matrix[l]<matrix[k]){
            l--;
        }

        /*positie k en l omwisselen*/
        temp = matrix[k];
        matrix[k] = matrix[l];
        matrix[l] = temp;

        /*vanaf k+1 t/m laatste alles omwisselen*/
        for(i=0;i<4.5-(k+1)/2;i++){
            temp = matrix[k+1+i];
            matrix[k+1+i] = matrix[9-i];
            matrix[9-i] = temp;
        }
    }

    for(i=0;i<10;i++){
        printf("%d",matrix[i]);
    }

    return 0;
}
