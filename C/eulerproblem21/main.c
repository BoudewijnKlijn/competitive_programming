#include <stdio.h>
#include <stdlib.h>

int sum_proper_divisors(number){
    int i, sum;
    sum = 0;
    for(i=1;i*i<number;i++){
        if (number%i == 0){
            if (i*i == number || i==1){
                sum += i;
            }
            else{
                sum += i + number/i;
            }
        }
    }
    return sum;
}

int main()
{
    int i,sum;
    int array[10000] = {0};

    sum = 0;

    for (i=1;i<10000;i++){
        array[i] = sum_proper_divisors(i);
        if (array[i] < i ){
            if (array[array[i]] == i){
                sum += i + array[i];
            }
        }
    }

    printf("answer: %d", sum);
    return 0;
}
