#include <stdio.h>
#include <stdlib.h>
#include <math.h>

int sum_digits(long long number){
    int sum=0;
    while (number>0){
        sum += number%10;
        number = number/10;
    }
    return sum;
}

int main()
{
    long long a_n=1, n=1;
    int extra=1, extra_mod=0, n_extra=0,lookup_ok=0,not_in_table=0;

    int c_mod=100, max_row=10, row=0, start_times=0, max_start_times=100, c_stop=0, go=1;
    long long lookup_start[1000][4] = {};
    long long lookup_stop[100][2] = {};

    int i, j;

    while(go){

        extra = sum_digits(a_n);

        if(a_n>c_mod*start_times && row<max_row && start_times<max_start_times){
            lookup_start[start_times*max_row+row][0] = n;
            lookup_start[start_times*max_row+row][1] = a_n;
            lookup_start[start_times*max_row+row][2] = extra;
            lookup_start[start_times*max_row+row][3] = a_n%c_mod;
            row++;
            if(row==max_row){
                start_times++;
                c_stop = 1;
            }
        }

        if(a_n+extra >= c_mod*start_times && c_stop==1){
            lookup_stop[start_times-1][0] = n;
            lookup_stop[start_times-1][1] = a_n;
            row = 0;
            c_stop = 0;
        }

        a_n += extra;
        n++;
        if(start_times==max_start_times && c_stop==0){
            printf("Table filled. a_%lld: %lld \n",n,a_n);
            break;
        }
    }

    printf("%\n\n");
    for(i=0;i<max_start_times*max_row;i++){
        printf("%d,",i);
        for(j=0;j<4;j++){
            printf("%lld,",lookup_start[i][j]);
        }
        printf("\n");
    }

    for(i=0;i<max_start_times;i++){
        printf("%d,",i);
        for(j=0;j<2;j++){
            printf("%lld,",lookup_stop[i][j]);
        }
        printf("\n");
    }

    printf("%lld,%lld,%lld,%lld,",lookup_start[439][0],lookup_start[439][1],lookup_start[439][2],lookup_start[439][3]);
    printf("%lld,%lld,",lookup_stop[439/10][0],lookup_stop[439/10][1]);

    go = 0;
    while(go){

        extra = sum_digits(a_n);
        extra_mod = a_n%c_mod;
        lookup_ok=0;

        for(i=0;i<max_row*max_start_times;i++){
            if(extra == lookup_start[i][2] && extra_mod == lookup_start[i][3]){
                printf("\ni: %d",i);
                n += lookup_stop[i/max_row][0] - lookup_start[i][0];
                a_n +=  lookup_stop[i/max_row][1] - lookup_start[i][1];

                printf("\nv2: a_%lld = %lld",n,a_n);
                lookup_ok = 1;

                break;
            }
        }
        if(lookup_ok==0){
            printf("\nnot in table+1, n=%lld, a_n=%lld",n,a_n);
            not_in_table++;

            a_n += extra;
            n++;
            printf("\nv1: a_%lld = %lld",n,a_n);
        }


        if(n>1600){
            break;
        }
    }



    printf("\n\na_%lld = %lld \n",n,a_n);
    return 0;
}

