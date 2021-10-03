#include <stdio.h>
#include <stdlib.h>

int is_pandigit(int i, int j, int k){
    int array[10] = {};
    int temp, sum = 0;
    while(i>0){
        temp = i%10;
        if(temp != 0 && array[temp]==0){
            array[temp]++;
            sum++;
            i /= 10;
        }
        else{
            return 0;
        }
    }
    while(j>0){
        temp = j%10;
        if(temp != 0 && array[temp]==0){
            array[temp]++;
            sum++;
            j /= 10;
        }
        else{
            return 0;
        }
    }
    while(k>0){
        temp = k%10;
        if(temp != 0 && array[temp]==0){
            array[temp]++;
            sum++;
            k /= 10;
        }
        else{
            return 0;
        }
    }
    if(sum==9){
        return 1;
    }
}

int main()
{
    int i,j,k=0,ij,l,sum=0,array[100]={0};

    for(i=1;i<100;i++){
        for(j=100;j<10000;j++){
            ij = i*j;
            if(is_pandigit(i,j,ij)){
                if(k==0){
                    array[k] = ij;
                    sum += ij;
                    k++;
                }
                else{
                    for(l=0;l<k;l++){
                        if(array[l]==ij){
                            break;
                        }
                        else if(l==k-1){
                            array[k] = ij;
                            sum += ij;
                            k++;
                        }
                    }
                }
            }
        }
    }
    printf("%d",sum);
    return 0;
}
