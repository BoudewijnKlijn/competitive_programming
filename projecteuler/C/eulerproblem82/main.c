#include <time.h>
#include <stdio.h>
#include <stdlib.h>

#define MAX_ROW 80
#define MAX_COL 80

/*answer 260342, runs instantly*/

int main()
{
    int row=0, col=0, x, matrix[MAX_ROW][MAX_COL]={}, temp[MAX_ROW][MAX_COL]={}, minimum, sum, alt_row_start, alt_row;

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

    for(col=1;col<MAX_COL-1;col++){
        for(row=0;row<MAX_ROW;row++){
            minimum = matrix[row][col-1];
            for(alt_row_start=0;alt_row_start<MAX_ROW;alt_row_start++){
                sum = matrix[alt_row_start][col-1];
                if(alt_row_start<row){
                    for(alt_row=alt_row_start;alt_row<row;alt_row++){
                        sum += matrix[alt_row][col];
                    }
                }else if(alt_row_start>row){
                    for(alt_row=alt_row_start;alt_row>row;alt_row--){
                        sum += matrix[alt_row][col];
                    }
                }
                if(sum<minimum){
                    minimum = sum;
                }
            }
            temp[row][col] = minimum;
        }
        for(row=0;row<MAX_ROW;row++){
            matrix[row][col] += temp[row][col];
        }
    }
    col=MAX_COL-1;
    minimum = matrix[0][MAX_COL-1] + matrix[0][MAX_COL-2];
    for(row=0;row<MAX_ROW;row++){
        matrix[row][col] += matrix[row][col-1];
        if(matrix[row][col]<minimum){
            minimum = matrix[row][col];
        }
    }


    printf("%d\n\n",minimum);

    clock_t end = clock();
    double time_spent = (double)(end - begin) / CLOCKS_PER_SEC;
    printf("Elapsed time in seconds: %.20f",time_spent);

    return 0;
}
