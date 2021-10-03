#include <stdio.h>
#include <stdlib.h>

int is_pandigit(long long number, int n){
    int array[10] = {0}, temp, sum = 0;
    while(number>0){
        temp = number%10;
        if(array[temp]>0){
            break;
        }
        sum++;
        array[temp]++;
        number /= 10;
    }
    if(sum!=n+1){
        return 0;
    }
    return 1;
}


/*duurt erg lang: 10 min, en kan ook gewoon met de hand opgelost worden door alles weg te strepen en de 6 getalen bij elkaar op te tellen.
antwoord: 16695334890 */
int main()
{
    long long i,temp,sum = 0;
    int s17,s13,s11,s7,s5,s3,s2;

    for(i=123456789;i<9876543211;i++){
        if(is_pandigit(i,9)){
            temp = i;
            s17 = temp%1000;
            if(s17%17==0){
                temp /= 10;
                s13 = temp%1000;
                if(s13%13==0){
                    temp /= 10;
                    s11 = temp%1000;
                    if(s11%11==0){
                        temp /= 10;
                        s7 = temp%1000;
                        if(s7%7==0){
                            temp /= 10;
                            s5 = temp%1000;
                            if(s5%5==0){
                                temp /= 10;
                                s3 = temp%1000;
                                if(s3%3==0){
                                    temp /= 10;
                                    s2 = temp%1000;
                                    if(s2%2==0){
                                        sum += i;
                                        printf("%lld",i);
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
    printf("answer: %lld\n",sum);
    return 0;
}
