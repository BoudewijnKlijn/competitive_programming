#include <stdio.h>
#include <stdlib.h>

int is_prime(long long number){
    int i;
    if(number<2){
        return 0;
    }
    for(i=2;i*i<=number;i++){
        if(number%i==0){
            return 0;
        }
    }
    return 1;
}

int is_pandigit(long long number, int n){
    int array[10] = {0}, temp, sum = 0;
    while(number>0){
        temp = number%10;
        if(temp<1 || temp > n || array[temp]>0){
            break;
        }
        sum++;
        array[temp]++;
        number /= 10;
    }
    if(sum!=n){
        return 0;
    }
    return 1;
}

long long absolute(long long number){
    if(number<0){
        number *= -1;
    }
    return number;
}

int number_of_digits(long long number){
    int x = 0;
    number = absolute(number);
    while(number>0){
        number /= 10;
        x++;
    }
    return x;
}

int main()
{
    int i=987654321;
    while (1==1){
        int n = number_of_digits(i);
        if(is_pandigit(i,n)){
            if(is_prime(i)){
                break;
            }
        }
        i-=2;
    }
    printf("answer: %d",i);/*7652413*/
    return 0;
}
