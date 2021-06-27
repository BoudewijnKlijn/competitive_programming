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

long long power(int number, int p){
    int i;
    long long x = 1;
    for(i=0;i<p;i++){
        x *= number;
    }
    return x;
}

int same_digits(int n1, int n2, int n3){
    int v1=0,v2=0,v3=0;
    while(n1>0){
        v1 += power(2,n1%10);
        n1 /= 10;
    }
    while(n2>0){
        v2 += power(2,n2%10);
        n2 /= 10;
    }
    while(n3>0){
        v3 += power(2,n3%10);
        n3 /= 10;
    }
    if(v1==v2 && v1==v3){
        return 1;
    }
    return 0;
}

int main()
{
    int i,inc;

    for(inc=1;inc<5000;inc++){
        for(i=1000;i<9999-2*inc;i++){
            if(is_prime(i)&&is_prime(i+inc)&&is_prime(i+2*inc)){
                if(same_digits(i,i+inc,i+2*inc)==1){
                    printf("answer: %d%d%d\n",i,i+inc,i+2*inc);
                }
            }
        }
    }
    return 0;
}
