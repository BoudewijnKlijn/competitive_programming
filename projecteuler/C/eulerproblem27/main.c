#include <stdio.h>
#include <stdlib.h>

int is_prime(int number){
    int i;
    if (number<0){
        number *= -1;
    }
    for(i=2;i*i<=number;i++){
        if(number%i==0){
            return 0;
        }
    }
    return 1;
}

int length_consecutive_primes(int a, int b){
    int sum = 0;
    int n = 0;

    while(is_prime(n*n+a*n+b)){
          n++;
          sum++;
    }
    return sum;
}

int main()
{
    int a,b,n,l;
    int best = 0;
    int most = 0;

    for(a=-999;a<1000;a++){
        for(b=-999;b<1000;b++){
            l = length_consecutive_primes(a,b);
            if(l>most){
                most = l;
                best = a*b;
            }
        }
    }
    printf("%d",best);
    return 0;
}
