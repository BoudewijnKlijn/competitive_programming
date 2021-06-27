#include <stdio.h>
#include <stdlib.h>

int main()
{
    int i, j, x, row, col, tally, k;
    int data[100][50];
    int som[52];

    FILE *fp;
    fp=fopen("C:\\Users\\BOUDEWIJN\\projecteuler-C\\eulerproblem13\\input.txt", "r");

    row = 0;
    col = 0;

    while  ( ( x = fgetc( fp ) ) != EOF ){
        if( x == '\n'){
            col = 0;
            row++;
        }
        else{
            data[row][col] = x - '0';
            col++;
        }
    }
    fclose(fp);

    tally = 0;
    for(i=49;i>=0;i--){
        for(j=0;j<=99;j++){
            tally += data[j][i];
        }
        som[i+2] = tally%10;
        tally /= 10;
    }
    som[1] = tally%10;
    tally /= 10;
    som[0] = tally%10;

    printf( "first 10 digits are: ");
    for (k=0;k<=9;k++){
        printf( "%d", som[k]);
    }

    return 0;
}
