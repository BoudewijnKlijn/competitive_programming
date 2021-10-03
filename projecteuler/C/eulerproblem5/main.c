#include <stdio.h>
#include <stdlib.h>

int main()
{
    int divider_low, divider_high, go, number, i;

    divider_low = 11;
    divider_high = 20;
    go = 1;
    number = 2520;

    while (go == 1){
        number += 2520;
        for(i=divider_low;i<=divider_high;i++){
            if (number%i == 0){
                if(i==divider_high){
                    go = 0;
                    printf("%d",number);
                    break;
                }
            }
            else{
                break;
            }
        }
    }
    return 0;
}
