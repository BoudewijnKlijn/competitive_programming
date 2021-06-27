#include <stdio.h>
#include <stdlib.h>

int power(int number, int p){
    int i,n = number;
    for(i=1;i<p;i++){
        number *= n;
    }
    return number;
}

int first_digit(int number){
    while(number>9){
        number /= 10;
    }
    return number;
}

int contains_even_number(int number){
    while(number>0){
        if(number%2==0){
            return 1;
        }
        number /= 10;
    }
    return 0    ;
}

int is_prime(int number){
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
    int i,j,temp,n,first,sum = 0,k;
    for(i=2;i<1000000;i++){
        if(is_prime(i)){
            n = 0;
            temp = i;
            while(temp>0){
                temp /= 10;
                n++;
            }
            if(n==1){
                sum++;
                printf("%d\n",i);
            }
            else if(n>1 && !contains_even_number(i)){
                temp = i;
                for(k=1;k<n;k++){
                    first = first_digit(temp);
                    temp = (temp%(power(10,n-1)))*10 + first;
                    if(!is_prime(temp)){
                        break;
                    }
                    else if(k==n-1){
                        sum++;
                        printf("%d\n",i);
                    }
                }
            }
        }
    }
    printf("answer: %d",sum);
    return 0;
}
