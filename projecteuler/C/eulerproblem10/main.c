#include <stdio.h>
#include <stdlib.h>

int is_prime(int check){
    long long i;
    int return_value;

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
    long long i, sum;

    sum = 2;

    for(i=3;i<2000000;i+=2){
        if(is_prime(i)){
            sum += i;
        }
    }
    printf("%lld",sum);
    return 0;
}
