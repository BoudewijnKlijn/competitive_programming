#include <stdio.h>
#include <stdlib.h>

int main()
{
    int i,x,result=0,array[50] = {0};
    for(i=1;i<50;i++){
        array[i] = 0.5*i*(i+1);
    }

    FILE *fp;
    fp=fopen("C:\\Users\\BOUDEWIJN\\projecteuler-C\\eulerproblem42\\input.txt", "r");

    int sum = 0;
    while( (x = fgetc(fp)) != EOF ){

        if(x==','){
            sum = 0;
        }
        else if(x=='"'){
            for(i=1;i<50;i++){
                if(sum==array[i]){
                    result++;
                    break;
                }
                else if(array[i]>sum){
                    break;
                }
            }
        }
        else{
            sum += x - 'A' + 1;
        }
    }

    fclose(fp);

    printf("answer: %d",result);
    return 0;
}
