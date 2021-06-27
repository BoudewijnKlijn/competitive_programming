#include <stdio.h>
#include <stdlib.h>

int main()
{
    int i,j,k,x,number;
    number = 99*99;
    int possib2[6*99] = {0};
    int possib3[4*99] = {0};
    int possib5[2*99] = {0};
    int possib6[2*99] = {0};
    int possib7[2*99] = {0};
    int possib10[2*99] = {0};


    /*correction for doubles*/
    /*2,4,8,16,64*/
    x = 0;
    for(i=1;i<=6;i++){
        for(j=2;j<=100;j++){
            for(k=0;k<=x;k++){
                if (possib2[k]==j*i){
                    break;
                }
                else if(x==k){
                    possib2[x] = i*j;
                    x++;
                    break;
                }
            }
        }
    }
    number += x - 6*99;

    /*3,9,27,81*/
    x = 0;
    for(i=1;i<=4;i++){
        for(j=2;j<=100;j++){
            for(k=0;k<=x;k++){
                if (possib3[k]==j*i){
                    break;
                }
                else if(x==k){
                    possib3[x] = i*j;
                    x++;
                    break;
                }
            }
        }
    }
    number += x - 4*99;

    /*5,25*/
    x = 0;
    for(i=1;i<=2;i++){
        for(j=2;j<=100;j++){
            for(k=0;k<=x;k++){
                if (possib5[k]==j*i){
                    break;
                }
                else if(x==k){
                    possib5[x] = i*j;
                    x++;
                    break;
                }
            }
        }
    }
    number += x - 2*99;

    /*6,36*/
    x = 0;
    for(i=1;i<=2;i++){
        for(j=2;j<=100;j++){
            for(k=0;k<=x;k++){
                if (possib6[k]==j*i){
                    break;
                }
                else if(x==k){
                    possib6[x] = i*j;
                    x++;
                    break;
                }
            }
        }
    }
    number += x - 2*99;

    /*7,49*/
    x = 0;
    for(i=1;i<=2;i++){
        for(j=2;j<=100;j++){
            for(k=0;k<=x;k++){
                if (possib7[k]==j*i){
                    break;
                }
                else if(x==k){
                    possib7[x] = i*j;
                    x++;
                    break;
                }
            }
        }
    }
    number += x - 2*99;

    /*10,100*/
    x = 0;
    for(i=1;i<=2;i++){
        for(j=2;j<=100;j++){
            for(k=0;k<=x;k++){
                if (possib10[k]==j*i){
                    break;
                }
                else if(x==k){
                    possib10[x] = i*j;
                    x++;
                    break;
                }
            }
        }
    }
    number += x - 2*99;


    printf("%d",number);

    return 0;
}
