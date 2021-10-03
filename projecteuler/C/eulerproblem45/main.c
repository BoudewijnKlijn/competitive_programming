#include <stdio.h>
#include <stdlib.h>

int main(){
    int p=165,h=143;
    long long P=40755,H=40755;

    while(1==1){
        p++;
        P += 3*p - 2;
        if(H<P){
            h++;
            H += 4*h - 3;
        }
        if(P==H){
            printf("answer: %lld\n",P);
            return 0;
        }
    }
}

/*
#include <time.h>
int main()
{
    int p=165,h=143;
    long long P=40755,H=40755;

    clock_t begin, end;
    double time_spent;

    begin = clock();

    while(1==1){
        p++;
        P += 3*p - 2;
        if(H<P){
            h++;
            H += 4*h - 3;
        }
        if(P==H){
            printf("answer: %lld\n",P);

            end = clock();
            time_spent = (double)(end - begin) / CLOCKS_PER_SEC * 1000;
            printf("%g ms",time_spent);
            return 0;
        }
    }
}
*/
