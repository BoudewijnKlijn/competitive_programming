#include <stdio.h>
#include <stdlib.h>

int main()
{
    int i, som;

    som = 0;
    for(i=0;i<1000;i++){
        if(i%3==0 || i%5 == 0){
            som += i;
        }
    }
    return som;
}
