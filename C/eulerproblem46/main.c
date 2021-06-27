#include <stdio.h>
#include <stdlib.h>

int is_prime(long long number){
    int i;
    for(i=2;i*i<=number;i++){
        if(number%i==0){
            return 0;
        }
    }
    return 1;
}

int main()
{
    int j,not, i;

    for(i=9;1==1;i+=2){
        if(!is_prime(i)){
            not = 1;
            for(j=1;2*j*j<i;j++){
                if(is_prime(i-2*j*j)){
                    not = 0;
                    break;
                }
            }
            if(not==1){
                printf("answer: %d\n",i);
                return 0;
            }
        }
    }
    return 0;
}
