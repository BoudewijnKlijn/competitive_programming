#include <stdio.h>
#include <stdlib.h>
#include <time.h>

double** Make2DDoubleArray(int arraySizeX, int arraySizeY);
double** Make2DDoubleArray(int arraySizeX, int arraySizeY) {
    double** theArray;
    int i;
    theArray = (double**) malloc(arraySizeX*sizeof(double*));
    for (i = 0; i < arraySizeX; i++){
       theArray[i] = (double*) malloc(arraySizeY*sizeof(double));
    }
    return theArray;
}

long long concat(long long a, long long b);
long long concat(long long a, long long b){
    long c = b;
    while (c > 0) {
        a *= 10;
        c /= 10;
    }
    return a + b;
}

long long absolute(long long number);
long long absolute(long long number){
    if(number<0){
        number *= -1;
    }
    return number;
}

int is_prime(long long number);
int is_prime(long long number){
    int i;
    if(number<2){
        return 0;
    }
    for(i=2;i*i<=number;i++){
        if(number%i==0){
            return 0;
        }
    }
    return 1;
}

int number_of_digits(long long number);
int number_of_digits(long long number){
    int x = 0;
    number = absolute(number);
    while(number>0){
        number /= 10;
        x++;
    }
    return x;
}

long long power(int number, int p);
long long power(int number, int p){
    int i;
    long long x = 1;
    for(i=0;i<p;i++){
        x *= number;
    }
    return x;
}

int is_pandigit(long long number);
int is_pandigit(long long number){
    int array[10] = {0}, temp, sum = 0;
    while(number>0){
        temp = number%10;
        if(temp != 0 && array[temp]==0){
            array[temp]++;
            sum++;
            number /= 10;
        }
        else{
            return 0;
        }
    }
    if(sum==9){
        return 1;
    }
}

int get_digit_from_begin(long long number, int index);
int get_digit_from_begin(long long number, int index){
    int x = pow(10,index+1);
    while (number >= x){
        number /= 10;
    }
    return number%10;
}

long long binomial(int n,int k);
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

int main()
{



    /* #include <time.h> */
    clock_t begin, end;
    begin = clock();

    end = clock();
    printf("%g ms\n",(double)(end - begin)* 1000/CLOCKS_PER_SEC);

    return 0;
}
