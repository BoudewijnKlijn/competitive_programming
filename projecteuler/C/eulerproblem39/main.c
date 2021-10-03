#include <stdio.h>
#include <stdlib.h>
#include <math.h>

int main()
{
    int array[1001] = {0};
    int a,b,c,asq,bsq,csq,max=0,maxi=0,i;

    for(a=1;a<1000;a++){
        asq = a*a;
        for(b=a;b<1000;b++){
            if(a+b>1000){
                break;
            }
            bsq = b*b;
            c = sqrt(asq+bsq);
            if(a+b+c <= 1000 && c*c == asq+bsq){
                array[a+b+c]++;
            }
        }
    }
    for(i=1;i<1001;i++){
        if(array[i]>max){
            max = array[i];
            maxi = i;
        }
    }
    printf("%d",maxi);
    return 0;
}
