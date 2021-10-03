#include <stdio.h>
#include <stdlib.h>
#include <math.h>

/* index = 0 (first digit), index: = 1 (second digit) etc.*/
int get_digit_from_begin(int number, int index){
    while (number >= 10*pow(10,index)){
        number /= 10;
    }
    return number%10;
}

/* index = 0 (last digit), index: = 1 (second to last digit) etc.*/
int get_digit_from_end(int number, int index){
    number /= pow(10,index);
    return number%10;
}

int main()
{
    int multiplier_digits, lower, upper, number, go, i;

    multiplier_digits = 3;
    lower = pow(10, multiplier_digits - 1);
    upper = pow(10, multiplier_digits) - 1;
    number = upper*upper;
    go = 1;

    while (go == 1){
        number--;
        if (get_digit_from_begin(number,0) == get_digit_from_end(number,0) && get_digit_from_begin(number,1) == get_digit_from_end(number,1) && get_digit_from_begin(number,2) == get_digit_from_end(number,2)){
            for(i=lower;i<=upper;i++){
                if(number%i==0 && number/i >= lower && number/i <= upper){
                    go = 0;
                    break;
                }
            }
        }
    }
    printf("%d", number);

    return 0;
}
