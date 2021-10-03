#include <stdio.h>
#include <stdlib.h>

/* index = 0 (first digit), index: = 1 (second digit) etc.*/
int get_digit_from_begin(int number, int index){
    while (number >= 10*pow(10,index)){
        number /= 10;
    }
    return number%10;
}

int main()
{
    int i,x,som;
    int array[1001];
    for(i=0;i<=1000;i++){
        array[i] = 0;
    }
    array[0] = 3;
    array[1] = 3;
    array[2] = 5;
    array[3] = 4;
    array[4] = 4;
    array[5] = 3;
    array[6] = 5;
    array[7] = 5;
    array[8] = 4;
    array[9] = 3;
    array[10] = 6;
    array[11] = 6;
    array[12] = 8;
    array[13] = 8;
    array[14] = 7;
    array[15] = 7;
    array[16] = 9;
    array[17] = 8;
    array[18] = 8;

    x = 20;
    array[x-1] = 6;
    for(i=x+1;i<=x+9;i++){
        array[i-1] = array[x-1]+array[i-x-1];
    }
    x = 30;
    array[x-1] = 6;
    for(i=x+1;i<=x+9;i++){
        array[i-1] = array[x-1]+array[i-x-1];
    }
    x = 40;
    array[x-1] = 5;
    for(i=x+1;i<=x+9;i++){
        array[i-1] = array[x-1]+array[i-x-1];
    }
    x = 50;
    array[x-1] = 5;
    for(i=x+1;i<=x+9;i++){
        array[i-1] = array[x-1]+array[i-x-1];
    }
    x = 60;
    array[x-1] = 5;
    for(i=x+1;i<=x+9;i++){
        array[i-1] = array[x-1]+array[i-x-1];
    }
    x = 70;
    array[x-1] = 7;
    for(i=x+1;i<=x+9;i++){
        array[i-1] = array[x-1]+array[i-x-1];
    }
    x = 80;
    array[x-1] = 6;
    for(i=x+1;i<=x+9;i++){
        array[i-1] = array[x-1]+array[i-x-1];
    }
    x = 90;
    array[x-1] = 6;
    for(i=x+1;i<=x+9;i++){
        array[i-1] = array[x-1]+array[i-x-1];
    }

    for(i=100;i<=999;i++){
        if (i%100==0){
            array[i-1] = array[get_digit_from_begin(i,0)] + 7;
        }
        else{
            array[i-1] = array[get_digit_from_begin(i,0)] + 7 + 3 + array[i%100 -1];
        }

    }
    array[999] = 3 + 8;

    som = 0;
    for(i=0;i<1000;i++){
        som += array[i];
    }
    printf("%d",som);
    return 0;
}
