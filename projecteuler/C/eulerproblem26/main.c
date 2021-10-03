#include <stdio.h>
#include <stdlib.h>

/*find the same leftover*/
int cycle_length(int leftover[1001]){
    int i,j;
    int cycle = 0;

    for(i=0;i<1001;i++){
        j = i+1;
        for(j=i+1;j<1001;j++){
            if(leftover[i]==leftover[j]){
                cycle = j-i;
                return cycle;
            }
        }
    }
    return cycle;
}

int matrix[1000][1001] = {0};

int main()
{
    int i,j,d,l,dbegin,dend,longest,longest_d;
    int leftover[1001] = {0};

    longest = 0;
    longest_d = 0;

    dbegin = 2;
    dend = 999;

    for(d=dbegin;d<=dend;d++){
        leftover[0] = 10;
        for (i=1;i<1001;i++){
            matrix[d][i] = leftover[i-1]/d;
            leftover[i] = (leftover[i-1]%d)*10;
            if (leftover[i] == 0){
                i++;
                break;
            }

        }
        /*check for recurring cycle in leftover; long recurring cycle is only possible when leftover != 0*/
        if(leftover[i-1]!=0){
            l = cycle_length(leftover);
            if (l>longest){
                longest = l;
                longest_d = d;
            }
        }
    }

    printf("longest cycle for d: %d",longest_d);
    return 0;
}
