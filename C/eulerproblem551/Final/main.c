#include <stdio.h>
#include <stdlib.h>

int f_sum_digits(long long number){
    int sum=0;
    while (number>0){
        sum += number%10;
        number = number/10;
    }
    return sum;
}

int main()
{
    /*
    answer: 73597483551591773
    runtime: 2400 seconds
    c_mod = 10^8
    goal= 10^15
    */
    long long a_n=1, n=1;

    long long go=1, max_lookup_index=2000, c_mod=100000000, lookup_index=1, add_to_start=1, add_to_stop=0, sum_digits=1, value_less_mod=0;
    long long lookup_succes=0, lookup_succes_counter=0, n_steps_saved=0;

    long long lookup_start[2000][4] = {};
    long long lookup_stop[2000][2] = {};

    long long goal=1000000000000000;

    long long i, j;

    while(go){
        lookup_succes=0;

        sum_digits = f_sum_digits(a_n);
        value_less_mod = a_n%c_mod;

        if(add_to_start==1){
            for(i=1;i<lookup_index;i++){
                if( sum_digits==lookup_start[i][2] && value_less_mod==lookup_start[i][3]){

                    n += lookup_stop[i][0] - lookup_start[i][0];
                    a_n +=  lookup_stop[i][1] - lookup_start[i][1];

                    if(n>goal){
                        printf("Oops, too far... (%lld)\n",n-goal);
                        a_n -=  lookup_stop[i][1] - lookup_start[i][1];
                        n -= lookup_stop[i][0] - lookup_start[i][0];
                        go=0;
                        break;
                    }

                    n_steps_saved += lookup_stop[i][0] - lookup_start[i][0];

                    lookup_succes = 1;
                    lookup_succes_counter++;

                    break;
                }
            }
        }

        if( add_to_start==1 && a_n>c_mod*(lookup_index+lookup_succes_counter) ){
            lookup_start[lookup_index][0] = n;
            lookup_start[lookup_index][1] = a_n;
            lookup_start[lookup_index][2] = sum_digits;
            lookup_start[lookup_index][3] = value_less_mod;

            add_to_start=0;
            add_to_stop=1;
        }

        if( add_to_stop==1 && a_n+sum_digits>=c_mod*(lookup_index+1+lookup_succes_counter) ){
            lookup_stop[lookup_index][0] = n;
            lookup_stop[lookup_index][1] = a_n;

            add_to_start=1;
            add_to_stop=0;
            lookup_index++;
            if(lookup_index==max_lookup_index){
                printf("\nERROR: going out of bounds.\n");
                getchar();
                break;
            }
        }

        if(lookup_succes==0){
            a_n += sum_digits;
            n++;
        }

        if(n>goal){
            printf("\nERROR: too far.\n");
            go=1;
            break;
        }
    }

    while(n<goal){
        sum_digits = f_sum_digits(a_n);
        a_n += sum_digits;
        n++;
    }




    printf("%\n\n");
    for(i=1;i<lookup_index;i++){
        printf("%lld,",i);
        for(j=0;j<4;j++){
            printf("%lld,",lookup_start[i][j]);
        }
        printf(" - %lld,",i);
        for(j=0;j<2;j++){
            printf("%lld,",lookup_stop[i][j]);
        }
        printf("- - -");
    }

    printf("\n\n FINAL, n: %lld - a_n: %lld\n SAVED: %lld",n,a_n,n_steps_saved);
    return 0;
}

