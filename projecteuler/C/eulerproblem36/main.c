#include <stdio.h>
#include <stdlib.h>
#include <limits.h>

long long make_binary(long long number);
int * make_binary2(long long number);
int number_of_digits(long long number);
long long power(int number, int p);
int is_palindrome(long long number);
long long get_digit_from_end(long long number, int index);
long long get_digit_from_begin(long long number, int index);

int * make_binary2(long long number){
    int i = 0;
    static int binary[30] = {0};
    while(number>0){
        binary[i] = (number%2);
        number /= 2;
        i++;
    }
    binary[i] = 2;
    return binary;
}

int main()
{
    int i,j,x,sum = 0;
    int *binary;

    for(i=1;i<1000000;i+=2){
        if(is_palindrome(i)){
            binary = make_binary2(i);
            x=0;
            while(*(binary+x)!=2){
                x++;
            }
            for(j=0;j<x/2;j++){
                if (*(binary+j) != *(binary-j+x-1)){
                    break;
                }
            }
            if(j==x/2){
                sum += i;
            }
        }
    }
    printf("answer:%d",sum);
    return 0;
}

/* index = 0 (first digit), index: = 1 (second digit) etc.*/
long long get_digit_from_begin(long long number, int index){
    long long t = power(10,index+1);
    while (number >= t){
        number /= 10;
    }
    return number%10;
}

/* index = 0 (last digit), index: = 1 (second to last digit) etc.*/
long long get_digit_from_end(long long number, int index){
    number /= power(10,index);
    return number%10;
}

int is_palindrome(long long number){
    int j, n = number_of_digits(number);
    for(j=0;j<n/2;j++){
        if (get_digit_from_begin(number,j) != get_digit_from_end(number,j)){
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

int number_of_digits(long long number){
    int n = 0;
    while(number>0){
        number /= 10;
        n++;
    }
    return n;
}

long long make_binary(long long number){
    long long binary = 0;
    int i = 0;
    while(number>0){
        binary += (number%2)*power(10,i);
        number /= 2;
        i++;
    }
    return binary;
}
