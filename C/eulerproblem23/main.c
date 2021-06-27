#include <stdio.h>
#include <stdlib.h>

int sum_of_divisors(int number){
    int i,sum;
    sum = 0;
    for (i=1;i<number;i++){
        if(number%i==0){
            sum += i;
        }
    }
    return sum;
}

int main()
{
    int i,j,sum;
    int matrix[28123+1][3] = {0};

    for (i=1;i<=28123;i++){
        matrix[i][0] = sum_of_divisors(i);
        if (matrix[i][0]>i){
            matrix[i][1]=1;
        }
    }

    for(i=1;i<=28123;i++){
        if(matrix[i][1]==1){
            for(j=1;j<=28123;j++){
                if(matrix[j][1]==1 && i+j<=28123){
                    matrix[i+j][2] = 1;
                }
            }
        }
    }

    sum = 0;
    for(i=1;i<=28123;i++){
        if(matrix[i][2]==0){
            sum += i;
        }
    }

    printf("answer: %d",sum);

    return 0;
}
