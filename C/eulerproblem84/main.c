#include <stdio.h>
#include <stdlib.h>

#define N_DICE 6
#define N_SQUARE 40

void matrix_mult(double A[N_SQUARE][N_SQUARE], double B[N_SQUARE][N_SQUARE], double C[N_SQUARE][N_SQUARE]){
    int m,p,n;
    double sum;
    for(m=0;m<N_SQUARE;m++){
        for(p=0;p<N_SQUARE;p++){
            sum=0;
            for(n=0;n<N_SQUARE;n++){
                sum += A[m][n]*B[n][p];
            }
            C[m][p]=sum;
        }
    }
}

int main()
{
    double max, sum, roll_chance[1+2*N_DICE]={}, three_doubles_chance;
    double P[N_SQUARE][N_SQUARE]={};
    double P_dum[N_SQUARE][N_SQUARE]={};
    double P_end[N_SQUARE][N_SQUARE]={};

    int i, j, max_index, from_sq, square, P_power, count, runs, roll;

    /*create roll probabilities*/
    for(i=1;i<=N_DICE;i++){
        for(j=1;j<=N_DICE;j++){
            roll_chance[i+j] += 1.0/(N_DICE*N_DICE);
        }
    }

    /*create initial markov chain probabilities*/
    for(from_sq=0;from_sq<N_SQUARE;from_sq++){
        for(roll=2;roll<=2*N_DICE;roll++){
            P[from_sq][(from_sq+roll)%N_SQUARE] += roll_chance[roll];
        }
    }

    /*Adjust for: go to jail square[30]*/
    for(from_sq=0;from_sq<N_SQUARE;from_sq++){
        P[from_sq][10] += P[from_sq][30];
        P[from_sq][30] = 0;
    }

    /*Adjust for: 3 doubles in a row*/
    three_doubles_chance = 1.0/(N_DICE*N_DICE*N_DICE);
    for(from_sq=0;from_sq<N_SQUARE;from_sq++){
        for(square=0;square<N_SQUARE;square++){
            if(square!=10 && from_sq!=10){
                P[from_sq][10] += P[from_sq][square]*three_doubles_chance;
                P[from_sq][square] = P[from_sq][square]*(1.0-three_doubles_chance);
            }
        }
    }

    /*Adjust for: CH cards*/
    for(from_sq=0;from_sq<N_SQUARE;from_sq++){
        P[from_sq][0] += (P[from_sq][7]+P[from_sq][22]+P[from_sq][36])/16.;
        P[from_sq][10] += (P[from_sq][7]+P[from_sq][22]+P[from_sq][36])/16.;
        P[from_sq][11] += (P[from_sq][7]+P[from_sq][22]+P[from_sq][36])/16.;
        P[from_sq][24] += (P[from_sq][7]+P[from_sq][22]+P[from_sq][36])/16.;
        P[from_sq][39] += (P[from_sq][7]+P[from_sq][22]+P[from_sq][36])/16.;
        P[from_sq][5] += (P[from_sq][7]+P[from_sq][22]+P[from_sq][36])/16.;
        P[from_sq][5] += P[from_sq][36]*2./16.;
        P[from_sq][15] += P[from_sq][7]*2./16.;
        P[from_sq][25] += P[from_sq][22]*2./16.;
        P[from_sq][12] += (P[from_sq][7]+P[from_sq][36])/16.;
        P[from_sq][28] += P[from_sq][22]/16.;
        P[from_sq][4] += P[from_sq][7]/16.;
        P[from_sq][19] += P[from_sq][22]/16.;
        P[from_sq][33] += P[from_sq][36]/16.;

        P[from_sq][7] = P[from_sq][7]*3./8.;
        P[from_sq][22] = P[from_sq][22]*3./8.;
        P[from_sq][36] = P[from_sq][36]*3./8.;
    }

    /*Adjust for: CC cards*/
    for(from_sq=0;from_sq<N_SQUARE;from_sq++){
        P[from_sq][0] += (P[from_sq][2]+P[from_sq][17]+P[from_sq][33])/16.;
        P[from_sq][10] += (P[from_sq][2]+P[from_sq][17]+P[from_sq][33])/16.;
        P[from_sq][2] = P[from_sq][2]*7./8.;
        P[from_sq][17] = P[from_sq][17]*7./8.;
        P[from_sq][33] = P[from_sq][33]*7./8.;
    }

    /*brute force steady state*/
    for(i=0;i<N_SQUARE*N_SQUARE;i++){
        *(P_end[0]+i)=*(P[0]+i);
    }
    count=0;
    runs=0;
    while(count!=N_SQUARE*N_SQUARE){
        runs++;
        matrix_mult(P,P_end,P_dum);
        count=0;
        for(i=0;i<N_SQUARE*N_SQUARE;i++){
            if( (*(P_end[0]+i)-*(P_dum[0]+i))*(*(P_end[0]+i)-*(P_dum[0]+i)) < 0.0000000001 ){
                count++;
            }
            *(P_end[0]+i)=*(P_dum[0]+i);
        }
    }

    /*display steady state
    for(i=0;i<N_SQUARE*N_SQUARE;i++){
        if(i%N_SQUARE==0){
            printf("\n");
        }
        printf("%.3f-",*(P_end[0]+i)*100);
    }*/

    printf("\nRuns until steady state: %d.\n\n",runs);

    /*find and display 3 largest values, also verify sum of row=1*/
    sum=0;
    max=0;
    for(j=1;j<=3;j++){
        for(from_sq=0;from_sq<N_SQUARE;from_sq++){
            if(j==1){
                sum += *(P_end[0]+from_sq);
            }
            if( *(P_end[0]+from_sq)>max ){
                max=*(P_end[0]+from_sq);
                max_index=from_sq;
            }

        }
        printf("max: %0.5f, index: %d\n",max*100,max_index);
        *(P_end[0]+max_index)=0.;
        max=0;
    }
    printf("Sum must be equal to 1. Sum: %0.10f\n",sum);

    return 0;
}
