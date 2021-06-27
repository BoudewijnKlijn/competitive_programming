#include <stdio.h>
#include <stdlib.h>

#define MAX_INDEX 200
int main()
{
    int number[MAX_INDEX]={}, a, b, i, answer=0, sum, remainder, dummy;

    for(a=1;a<100;a++){

        for(i=MAX_INDEX-1;i>=0;i--){
           number[i] = 0;
        }
        number[MAX_INDEX-1] = a;
        remainder = 0;
        for(b=1;b<100;b++){
            for(i=MAX_INDEX-1;i>=0;i--){
                dummy = number[i]*a + remainder;
                number[i] = dummy%10;
                remainder = dummy/10;
            }

            sum=0;
            for(i=MAX_INDEX-1;i>=0;i--){
                sum += number[i];
            }

            if(sum>answer){
                answer = sum;
            }
        }
    }
    printf("Answer: %d",answer);
    return 0;
}
