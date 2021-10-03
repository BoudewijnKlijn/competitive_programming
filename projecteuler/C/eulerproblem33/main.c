#include <stdio.h>
#include <stdlib.h>

int main()
{
    int num,den,den1,den2,num1,num2;

    for(den=10;den<100;den++){
        den2 = den%10;
        den1 = (den/10)%10;
        for(num=10;num<den;num++){
            num2 = num%10;
            num1 = (num/10)%10;
            if(num2==0&&den1==0){
                break;
            }
            else if(num2==den1&&num*den2==den*num1){
                printf("%d/%d = %d/%d\n",num,den,num1,den2);
            }
        }
    }
    printf("LCM met de hand uitrekenen geeft antwoord: 100.\n");
    return 0;
}
