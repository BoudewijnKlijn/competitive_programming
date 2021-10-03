#include <stdio.h>
#include <stdlib.h>

int main()
{
    int i, j, x, row, col, last_was_digit, n;
    n = 15;
    int data[n][n];

    for(i=0;i<n;i++){
        for(j=0;j<n;j++){
            data[i][j] = 0;
        }
    }

    FILE *fp;
    fp=fopen("C:\\Users\\BOUDEWIJN\\projecteuler-C\\eulerproblem18\\input.txt", "r");

    row = 0;
    col = 0;

    while  ( ( x = fgetc( fp ) ) != EOF ){
        if(x=='\n'){
            printf("\n");
            col = 0;
            row++;
            last_was_digit = 0;
        }
        else if(x==32){
            printf(" ");
            col++;
            last_was_digit = 0;
        }
        else{
            printf("%d", x - '0');

            if(!last_was_digit){
                data[row][col] = (x-'0')*10;
            }
            else{
                data[row][col] += (x-'0');
            }
            last_was_digit = 1;
        }
    }
    fclose(fp);

    printf("\n\n");
    for(i=0;i<n;i++){
        for(j=0;j<n;j++){
            printf("%d ",data[i][j]);
        }
        printf("\n");
    }

    for(row=n-1;row>=0;row--){
        for(col=0;col<row;col++){
            if(data[row][col]>data[row][col+1]){
                data[row-1][col] += data[row][col];
            }
            else{
                data[row-1][col] += data[row][col+1];
            }
        }
    }

    printf("\n\n");
    for(i=0;i<n;i++){
        for(j=0;j<n;j++){
            printf("%d ",data[i][j]);
        }
        printf("\n");
    }

    printf("\n\nanswer: %d\n",data[0][0]);


    return 0;
}
