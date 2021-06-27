#include <stdio.h>
#include <stdlib.h>

void bubblesort(int data[5163][20]){
    int i,j,k,l,temp;
    for(i=0;i<5163-1;i++){
        for(j=0;j<5163-i-1;j++){
            k = 0;
            while(data[j][k]==data[j+1][k]){
                k++;
            }
            if(data[j][k]>data[j+1][k]){
                for (l=0;l<20;l++){
                    temp = data[j+1][l];
                    data[j+1][l] = data[j][l];
                    data[j][l] = temp;
                }
            }
        }
    }
}

int main()
{
    int x, i, j, row, col, totalscore;
    int array[5163][20] = {0};
    int *ptr;

    ptr = &array;

    FILE *fp;
    fp = fopen("C:\\Users\\BOUDEWIJN\\projecteuler-C\\eulerproblem22\\input.txt", "r");

    row = 0;
    col = 0;

    while( (x = fgetc(fp)) != EOF){
        if(x == ','){
            row++;
            col = 0;
        }
        else if(x != '"'){
            array[row][col] = x - 64;
            col++;
        }
    }
    fclose(fp);

    bubblesort(array);

    totalscore = 0;
    for(i=0;i<sizeof(array)/sizeof(int)/20;i++){
        j = 0;
        while(array[i][j] != 0){
            totalscore += (i+1)*array[i][j];
            j++;
        }
    }

    printf("answer: %d", totalscore);

    return 0;
}
