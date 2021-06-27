#include <stdio.h>
#include <stdlib.h>

int main()
{
    int year, month, day, correct, day_of_week, max_day;
    correct = 0;
    day_of_week = 3-1; /*1 jan 1901 was een woensdag, maar day_of_week++ staat bovenaan in de loop, dus start met -1.*/

    for (year=1901;year<2001;year++){
        for (month=1;month<13;month++){
            if(month==4 || month==6 || month==9 || month==11 ){
                max_day = 30;
            }
            else if(month == 2){
                max_day = 28;
                if (year%4 == 0){
                    max_day = 29;
                    if (year%100== 0){
                        max_day = 28;
                        if (year%400){
                            max_day = 29;
                        }
                    }
                }
            }
            else{
                max_day = 31;
            }
            for (day=1;day<=max_day;day++){
                day_of_week++;
                if (day_of_week>7){
                    day_of_week = 1;
                }
                if (day_of_week == 1 && day == 1){
                    correct++;
                }
            }
        }
    }

    printf("%d", correct);
    return 0;
}
