#include <stdio.h>
#include <stdlib.h>

int power(int number, int p){
    int i;
    int temp = number;
    for(i=2;i<=p;i++){
        temp *= number;
    }
    return temp;
}

int main()
{
    int i,sum,temp,number,j;
    long long total_sum = 0;

    for(i=1;i<1000000;i++){
        sum = 0;
        temp = i;
        while(temp!=0){
            number = temp%10;
            sum += power(number,5);;
            temp /= 10;
        }
        if(sum==i){
            total_sum += i;
        }
    }
    printf("answer: %lld",total_sum-1);
    return 0;
}
