#include <stdio.h>
#include <stdlib.h>

int order_digits(int * pointer, int digits){
    int i,j,dummy;
    for(j=0;j<digits;j++){
        for(i=0;i<digits-j-1;i++){
            if(pointer[i]>pointer[i+1]){
                dummy=pointer[i];
                pointer[i]=pointer[i+1];
                pointer[i+1]=dummy;
            }
        }
    }
}

int f_count_digits(long long number){
    int digits = 0;
    while (number>0){
        number = number/10;
        digits++;
    }
    return digits;
}

int create_number_array(long long number, int digits, int * p){
    int i;

    if(digits>0){
        for(i=1;i<=digits;i++){
            p[digits-i] = number%10;
            number = number/10;
        }
    }
}

int f_power(int base, int x){
    int i, result=1;
    for(i=1;i<=x;i++){
        result = result*base;
    }
    return result;
}

/*answer: 142857 in 0.1s*/
int main()
{
    int go=1, everything_ok, first_row=2, last_row=6, power=0, col;
    int number_array[8][15]={};
    int digits_array[8];
    long long row, number;

    long long addendum, start_number, end_number;

    while(go){

        addendum = f_power(10,power);
        start_number = 5*addendum;
        end_number = 17*addendum;

        for(number=start_number;number<end_number;number++){

            everything_ok=1;

            /*count digits of numbers and verify that they are all the same*/
            for(row=first_row;row<=last_row;row++){
                digits_array[row]=f_count_digits(number*row);
                if(row>first_row){
                    if(digits_array[row-1]!=digits_array[row]){
                        everything_ok=0;
                        break;
                    }
                }
            }

            /*create array of number, order the digits, and verify with previous number array*/
            if(everything_ok){
                 for(row=first_row;row<=last_row;row++){
                    create_number_array(number*row,digits_array[first_row],number_array[row]);
                    order_digits(number_array[row],digits_array[first_row]);

                    if(row>first_row){
                        for(col=0;col<digits_array[first_row];col++){
                            if(number_array[row][col]!=number_array[row-1][col]){
                                everything_ok=0;
                                break;
                            }
                        }
                        if(everything_ok==0){
                            break;
                        }
                    }
                }
            }

            if(everything_ok){
                printf("EUREKA!\nNumber:%lld",number);
                go=0;
                break;
            }

        }

        power++;
        if(power>10){
           go=0;
        }

    }

    return 0;
}
