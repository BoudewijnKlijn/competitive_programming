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

/*duurt lang (100s): antwoord is 997651*/
int main()
{
    int *primelist,i=1,j=0;
    primelist = malloc(100000*sizeof(int));
    while(j<100000){
        i++;
        if(is_prime(i)){
            primelist[j] = i;
            j++;
        }
    }

    int MAXI=0,MAX=0,start,sum;
    i=0;
    while(primelist[i]<1000000){
        for(start=0;start<i;start++){
            sum = 0;
            j = 0;
            while(sum<primelist[i]){
                sum += primelist[start+j];
                j++;
            }
            if(sum==primelist[i]){
                if(j>MAX){
                    MAX = j;
                    MAXI = primelist[i];
                }
                break;
            }
        }
        i++;
    }
    printf("answer: %d\n",MAXI);
    return 0;
}
