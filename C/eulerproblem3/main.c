#include <stdio.h>
#include <stdlib.h>

int is_prime(int check){
    int i, return_value;

    return_value = 1;

    for(i=2;i*i<=check;i++){
        if(check%i==0){
            return_value = 0;
            break;
        }
    }
    return return_value;
}

int main()
{
    long long number;
    int i, larg_div;

    number = 600851475143;
    i = 1;

    while (number > 1){
        i++;
        if (is_prime(i)){
            while(number%i==0){
                number = number/i;
                larg_div = i;
            }
        }
    }
    printf("%d", larg_div);
    return 0;
}
