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
    int count,i;

    count = 1;
    i = 1;

    while (count<10001){
        i += 2;
        if(is_prime(i)){
           count++;
        }
    }
    printf("10001th prime is %d ",i);
    return 0;
}
