#include <stdio.h>
#include <stdlib.h>

int is_prime(long long number){
    int i;
    for(i=2;i*i<=number;i++){
        if(number%i==0){
            return 0;
        }
    }
    return 1;
}

int main()
{
    int *primelist,length = 100000,i,j = 0;
    primelist = malloc(length*sizeof(int));
    for(i=2;j<length;i++){
        if(is_prime(i)){
            primelist[j]=i;
            j++;
        }
    }

    int n_consecutive=4,divisors[4]={0},temp,x=0,idiv,k,first;

    for(i=4;1==1;i++){
        for(j=0;j<n_consecutive;j++){
            temp = i+j;
            if(is_prime(temp)){
                break;
            }
            x=0;
            idiv = 0;
            while(temp>1){
                first = 1;
                while(temp%primelist[x]==0){
                    temp /= primelist[x];
                    if(first==1){
                        if(idiv<n_consecutive){
                            divisors[idiv] == primelist[x];
                            first = 0;
                        }
                        idiv++;
                    }
                }
                x++;
            }
            if(idiv!=n_consecutive){
                break;
            }
            if(j==n_consecutive-1){
                printf("answer: %d",i);
                return 0;
            }
        }
    }



    return 0;
}
