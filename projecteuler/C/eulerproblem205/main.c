#include <stdio.h>
#include <stdlib.h>

int main()
{
    int arrayP[36] = {0},P[9] = {1,1,1,1,1,1,1,1,1},i,j,c,leftover,sum;
    for(i=1;i<262144+1;i++){
        sum = 0;
        for(j=0;j<9;j++){
            sum += P[j];
        }
        arrayP[sum-1]++;

        leftover = 1;
        for(c=8;c>=0;c--){
            P[c] += leftover;
            leftover = 0;
            if(P[c]>4){
                P[c] = 1;
                leftover = 1;
            }
        }
    }

    int arrayC[36] = {0},C[6] = {1,1,1,1,1,1};
    for(i=1;i<46656+1;i++){
        sum = 0;
        for(j=0;j<6;j++){
            sum += C[j];
        }
        arrayC[sum-1]++;

        leftover = 1;
        for(c=5;c>=0;c--){
            C[c] += leftover;
            leftover = 0;
            if(C[c]>6){
                C[c] = 1;
                leftover = 1;
            }
        }
    }

    double prob = 0, temp1, temp2;
    int sumx = 0,p,x;
    for(p=0;p<36;p++){
        sumx = 0;
        for(x=0;x<p;x++){
            sumx += arrayC[x];
        }
        temp1 = sumx;
        temp2 = arrayP[p];
        prob += temp1/46656*temp2/262144;
    }

    printf("answer: %0.7f",prob);
    return 0;
}
