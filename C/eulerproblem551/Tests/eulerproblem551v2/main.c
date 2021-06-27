#include <stdio.h>
#include <stdlib.h>

int main()
{
    long long count = 1;
    int i, a_count[18]={0},sum_a_count,go=1;
    a_count[17]=1;

    while(go){
        sum_a_count = 0;
        count++;

        /*

        for(i=0;i<18;i++){
            sum_a_count += a_count[i];
            /*printf("%d",a_count[i]);
        }

        /*create new a_count
        for(i=17;i>=0;i--){
            a_count[i] += sum_a_count%10;
            sum_a_count = sum_a_count/10;
            if(a_count[i]>9){
                sum_a_count++;
                a_count[i] = a_count[i]-10;
            }
        }
        */
        if(count>=1000000000000){
            printf("a_%lld: ",count);
            for(i=0;i<18;i++){
                sum_a_count += a_count[i];
                printf("%d",a_count[i]);
            }
            break;
        }

    }
}
