#include <stdio.h>
#include <stdlib.h>


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

long long power(int number, int p){
    int i;
    long long x = 1;
    for(i=0;i<p;i++){
        x *= number;
    }
    return x;
}

int get_digit_from_begin(long long number, int index){
    long long x = power(10,index+1);
    while (number >= x){
        number /= 10;
    }
    return number%10;
}

int main()
{
    int i=0,j=0,total=0,product=1,index;
    int milestones[7] = {1,10,100,1000,10000,100000,1000000};

    while(j<=6){
        if(total+number_of_digits(i+1) >= milestones[j]){
            index = milestones[j] - total - 1;
            product *= get_digit_from_begin(i+1,index);
            j++;
        }
        i++;
        total += number_of_digits(i);
    }
    printf("answer: %d",product);
    return 0;
}
