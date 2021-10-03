#include <stdio.h>
#include <stdlib.h>
#include <math.h>

long long binomial(int n,int k);
double** Make2DDoubleArray(int arraySizeX, int arraySizeY);

long long binomial(int n,int k){
    if(k<0 || k>n){
        return 0;
    }
    if(k==0 || k==n){
        return 1;
    }
    long long r = 1,d;
    for(d=1;d<=k;d++){
      r *= n--;
      r /= d;
    }
    return r;
}

double** Make2DDoubleArray(int arraySizeX, int arraySizeY) {
    double** theArray;
    int i;
    theArray = (double**) malloc(arraySizeX*sizeof(double*));
    for (i = 0; i < arraySizeX; i++){
       theArray[i] = (double*) malloc(arraySizeY*sizeof(double));
    }
    return theArray;
}

int main(){

    double** value = Make2DDoubleArray(1000,1000);
    double a,b,cost=0,total_cost=0,max_cost;
    long long sum=0,n = 1000000000000;
    int i,j,k,col,row,low_cost_row,low_cost_col,F[31] = {0};
    int const ROWS = 1000, COLS = 1000;

    F[1] = 1;F[2] = 1;
    for(i=3;i<=30;i++){
        F[i] = F[i-1] + F[i-2];
    }

    for(k=1;k<=30;k++){
        a = sqrt(k);
        b = sqrt(F[k]);
        for(col=0;col<COLS;col++){
            for(row=col;row<ROWS;row++){
                value[row][col] = (row-col)*a + col*b;
            }
        }

        sum = 0;
        max_cost = (ROWS-COLS)*a + COLS*b;
        while(sum<n){
            cost = max_cost;
            low_cost_row = ROWS;
            low_cost_col = COLS/2;
            for(col=0;col<COLS;col++){
                for(row=col;row<ROWS;row++){
                    if(value[row][col]<cost && value[row][col]!= 0){
                        cost = value[row][col];
                        low_cost_row = row;
                        low_cost_col = col;
                    }
                }
            }
            sum += binomial(low_cost_row,low_cost_col);
            value[low_cost_row][low_cost_col] = 0;
        }
        total_cost += cost;
        printf("Subcost = %.8f\n",cost);
    }
    printf("Optimal strategy, worst cost = %.8f\n",total_cost);
    return 0;
}


/*

BRUTE FORCE: WORKS ONLY FOR EXAMPLES
int main()
{
    const double a=sqrt(5),b=sqrt(7);
    double cost_i,*cost_array,lowest,highest;
    cost_array = malloc(2000000*sizeof(double));
    int i,guess,max,imax=2000000+1,best=1,prev=1;

    for(i=2;i<imax;i++){
        max = (i+1)/2;
        cost_i = a + cost_array[i-1];

        for(guess=prev;guess<=prev+2;guess++){
            if( (a + cost_array[i-guess]) <= cost_i && (b + cost_array[guess-1]) <= cost_i ){
                best = guess;
                if( (a + cost_array[i-guess]) > (b + cost_array[guess-1])){
                    cost_i = (a + cost_array[i-guess]);
                }
                else{
                    cost_i = (b + cost_array[guess-1]);
                }
            }
        }
        prev = best;
        cost_array[i]=cost_i;
    }
    printf("Optimal strategy, worst cost: %.8f\n",cost_array[i-1]);
    return 0;
}
*/
