#include <stdio.h>
#include <stdlib.h>

/*answer 272, runs instantly*/
int main()
{
    int a, h[100]={}, hmin1[100]={}, hmin2[100]={}, max_col=99, i, answer=0, col, remainder, dummy;

    a=2;
    h[99]=2;
    hmin1[99]=1;
    hmin2[99]=0;

    for(i=2;i<=100;i++){
        if(i%3==0){
            a=(i/3)*2;
        }else{
            a=1;
        }

        remainder=0;
        for(col=max_col;col>=0;col--){
            hmin2[col] = hmin1[col];
            hmin1[col] = h[col];
            dummy = a*hmin1[col] + hmin2[col] + remainder;
            h[col] = dummy%10;
            remainder = dummy/10;
        }
    }

    for(col=max_col;col>=0;col--){
        answer+=h[col];
    }
    printf("Answer: %d",answer);
    return 1;
}
