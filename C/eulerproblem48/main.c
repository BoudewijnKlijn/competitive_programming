#include <stdio.h>
#include <stdlib.h>

int main()
{
    long long *array_i,*array_tot,i,j,temp,leftover,k;
    array_i = malloc(3000*sizeof(long long));
    array_tot = malloc(3000*sizeof(long long));

    for(i=0;i<3000;i++){
        array_i[i] = 0;
        array_tot[i] = 0;
    }

    for(i=1;i<1001;i++){
        array_i[3000-1] = i;
        leftover = 0;
        for(j=1;j<i;j++){
            for(k=3000-1;k>0;k--){
                temp = leftover + array_i[k]*i;
                array_i[k] = temp%10;

                leftover = temp/10;
            }
        }

        leftover = 0;
        for(k=3000-1;k>0;k--){
            temp = leftover + array_tot[k] + array_i[k];
            array_tot[k] = temp%10;
            leftover = temp/10;
            array_i[k] = 0;
        }
    }

    for(k=0;k<3000;k++){
        printf("%lld,",array_tot[k]);
    }
    return 0;
}
