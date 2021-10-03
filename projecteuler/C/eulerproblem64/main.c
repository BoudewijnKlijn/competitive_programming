#include <stdio.h>
#include <stdlib.h>

int get_floor(int b, int a2, int a1, int a02D){
    while((b+1)*(b+1)*a2*a2+a1*a1-2*a1*(b+1)*a2 <= a02D){
        b++;
    }
    return b;
}

int f_gcd(int a, int b, int c){
    int div=2, gcd=1;
    while(div<=a && div<=b && div<=c){
        if(a%div==0 && b%div==0 && c%div==0){
            gcd = gcd*div;
            a = a/div;
            b = b/div;
            c = c/div;
        }else{
            div++;
        }
    }
    return gcd;
}

int main()
{
    int D, b[1000]={},a0[1000]={},a1[1000]={},a2[1000]={}, gcd, found=0, i, max_i=999;
    int dummy, col, max_col=199, period, answer=0;
    for(D=1;D<=10000;D++){
        a0[0]=1;
        a1[0]=0;
        a2[0]=1;

        found=0;
        period=1;
        for(i=0;i<=max_i;i++){
            b[i] = get_floor(0,a2[i],a1[i],a0[i]*a0[i]*D);
            if(b[i]*b[i]==D){
                found=1;
                period=0;
                break;
            }

            a0[i+1]= a2[i]*a0[i];
            a1[i+1]= -a2[i]*(a1[i]-b[i]*a2[i]);
            a2[i+1]= a0[i]*a0[i]*D-(a1[i]-b[i]*a2[i])*(a1[i]-b[i]*a2[i]);

            /*numbers will get really big, so divide by greatest common divisor*/
            gcd = f_gcd(a0[i+1],a1[i+1],a2[i+1]);
            if(gcd>1){
                a0[i+1]= a0[i+1]/gcd;
                a1[i+1]= a1[i+1]/gcd;
                a2[i+1]= a2[i+1]/gcd;
            }
        }

        /*determine the period*/
        while(!found){
            for(i=1;i<=max_i-period;i++){
                if(b[i]!=b[i+period]){
                    period++;
                    break;
                }
                if(i==max_i-period){
                    found=1;
                    break;
                }
            }
        }

        if(period%2!=0){
            answer++;
        }
    }
    printf("Answer: %d",answer);
    return 0;
}
