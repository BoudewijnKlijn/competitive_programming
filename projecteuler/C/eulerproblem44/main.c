#include <stdio.h>
#include <stdlib.h>
#include <stdlib.h>

int main()
{
    int i,j,k,x,n;
    long long penti,pentj,N,X;

    for(i=1;1==1;i++){
        penti = i*(3*i-1)/2;
        for(j=i-1;j>0;j--){
            pentj = j*(3*j-1)/2;
            N = penti+pentj;
            n = (sqrt(24*N+1)+1)/6;
            if(N == n*(3*n-1)/2){
                X = penti-pentj;
                x = (sqrt(24*X+1)+1)/6;
                if(X == x*(3*x-1)/2){
                    printf("%lld",X);
                    return 0;
                }
            }
        }
    }
}
