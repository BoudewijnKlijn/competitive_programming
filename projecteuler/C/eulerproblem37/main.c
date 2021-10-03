#include <stdio.h>
#include <stdlib.h>

int is_prime(number){
    int i;
    for(i=2;i*i<=number;i++){
        if(number%i==0){
            return 0;
        }
    }
    return 1;
}

int power(int number, int p){
    int i;
    int x = 1;
    for(i=0;i<p;i++){
        x *= number;
    }
    return x;
}

int main()
{
    int i,j,sum = 0,minus_last,minus_first,in,x,temp;

    for(i=10;i<1000000;i++){
        if(is_prime(i)){
            temp = i;
            in = 1;
            while(temp>9 && in==1){
                minus_last = temp/10;
                temp /= 10;
                if(!is_prime(minus_last)||minus_last==1){
                    in = 0;
                }
            }
            temp = i;
            while(temp>9 && in==1){
                x = 1;
                while(temp/power(10,x)!=0){
                    x++;
                }
                minus_first = power(10,x-1) - (power(10,x)-temp)%power(10,x-1);
                temp = minus_first;
                if(!is_prime(minus_first)||minus_first==1){
                    in = 0;
                }
            }
            if(in==1){
                sum+=i;
            }
        }
    }
    printf("%d",sum);
    return 0;
}
