#include <stdio.h>
#include <stdlib.h>

int is_pandigit(int number){
    int array[10] = {0};
    int temp, sum = 0;
    while(number>0){
        temp = number%10;
        if(temp != 0 && array[temp]==0){
            array[temp]++;
            sum++;
            number /= 10;
        }
        else{
            return 0;
        }
    }
    if(sum==9){
        return 1;
    }
}

int create_number(int i,int n){
    long long number = 0;
    int j,x;
    for(j=n;j>0;j--){
        x = number_of_digits(number);
        if(x>8){
            return 1;
        }
        number += j*i*power(10,x);
    }
    return number;
}

int number_of_digits(long long number){
    int x = 0;
    if(number<0){
        number *= -1;
    }
    while(number>0){
        number /= 10;
        x++;
    }
    return x;
}

int power(int number, int p){
    int i;
    long long x = 1;
    for(i=0;i<p;i++){
        x *= number;
    }
    return x;
}



int main()
{
    int i,n,largest=0;
    long long number;

    for(i=1;i<10000;i++){
        for(n=2;n<10;n++){
            number = create_number(i,n);
            if(number==1||number_of_digits(number)>9||number<0){
                break;
            }
            else if(is_pandigit(number)){
                if(number>largest){
                    largest=number;
                }
            }
        }
    }
    printf("answer: %d",largest);
    return 0;
}
