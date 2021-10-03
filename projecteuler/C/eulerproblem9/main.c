#include <stdio.h>
#include <stdlib.h>

int main()
{
    int a, b, c, asq, bsq, csq, s;

    s = 1000;

    for(a=1;a<s/3;a++){
        asq = a*a;
        for(b=1;b<s/2;b++){
            bsq = b*b;
            for(c=1;c<s/2;c++){
                if(asq+bsq == c*c && a+b+c == s){
                    printf("%d",a*b*c);
                    return 0;
                }
            }
        }
    }
}
