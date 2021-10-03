#include <time.h>
#include <stdio.h>
#include <stdlib.h>

#define MAX_ROW 80
#define MAX_COL 80

int main()
{
    int row=0, col=0, x, matrix[MAX_ROW][MAX_COL]={};

    FILE *fp;
    fp=fopen("p081_matrix.txt", "r");
    int number = 0;

    while(1){
        x = fgetc(fp);
        if( feof(fp) ){
            break;
        }else if(x=='\n'){
            matrix[row][col] = number;
            number = 0;
            row++;
            col=0;
        }else if(x==','){
            matrix[row][col] = number;
            number = 0;
            col++;
        }else{
            number = number*10+(x-'0');
        }
    }
    fclose(fp);

    clock_t begin = clock();

    for(row=MAX_ROW-1;row>=0;row--){
        for(col=MAX_COL-1;col>=0;col--){
            if( col!=(MAX_COL-1) || row!=(MAX_ROW-1) ){
                if( row==(MAX_ROW-1)){
                    matrix[row][col] += matrix[row][col+1];
                }
                else if( col==(MAX_COL-1)){
                    matrix[row][col] += matrix[row+1][col];
                }
                else{
                    if(matrix[row+1][col] > matrix[row][col+1]){
                        matrix[row][col] += matrix[row][col+1];
                    }else{
                        matrix[row][col] += matrix[row+1][col];
                    }
                }

            }
        }
    }

    printf("%d\n\n",matrix[0][0]);

    clock_t end = clock();
    double time_spent = (double)(end - begin) / CLOCKS_PER_SEC;
    printf("Elapsed time in seconds: %.20f",time_spent);

    return 0;
}
