#include <stdio.h>
#include <stdlib.h>

int main()
{
    int gridsize, row, col;
    gridsize = 20;
    long long gridpoints[gridsize+1][gridsize+1];

    for(row=gridsize;row>=0;row--){
        for(col=gridsize;col>=0;col--){
            if(row == gridsize || col == gridsize){
                gridpoints[row][col] = 1;
            }
            else{
                gridpoints[row][col] = gridpoints[row+1][col] + gridpoints[row][col+1];
            }
        }
    }

    printf("%lld", gridpoints[0][0]);

    return 0;
}
