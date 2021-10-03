#include <stdio.h>
#include <stdlib.h>

int is_prime(long long number){
    long long i;

    if(number==2){
        return 1;
    }

    if(number%2==0){
        return 0;
    }

    for(i=3;i*i<=number;i+=2){
        if(number%i==0){
            return 0;
        }
    }
    return 1;
}

int power(int base, int x){
    int i, result=1;
    for(i=1;i<=x;i++){
        result = result*base;
    }
    return result;
}

int f_count_digits(long long number){
    int digits = 0;
    while (number>0){
        number = number/10;
        digits++;
    }
    return digits;
}

int create_number_array(long long number, int digits, int * p){
    int i;

    if(digits>0){
        for(i=1;i<=digits;i++){
            p[digits-i] = number%10;
            number = number/10;
        }
    }
}

int array_to_int(int digits, int array[]){
    int i;
    long long number = 0;

    if(digits>0){
        for(i=0;i<digits;i++){
            number = number*10 + array[i];
        }
    }
    return number;
}

/*answer: 121313 for 8*/
/*answer: 38000201 for 9*/

int main()
{
    long long number=1, new_number=0;
    int go=1, digits, number_array[100]={0}, number_array_copy[100]={0};
    int * pointer;

    int goal=8, ten_min_goal=10-goal;

    int search, position, good, wrong, instances, possibilities, combination, leftover, replacement, help_position,i,j,help_sum;

    pointer = &number_array;

    int help_array[1014][10] = {{1,2,4,8,16,32,64,128,256,512}}; /*2^10=1024 minus 10 (2^0,2^1....2^9) minus 0 (0) plus 1 for top row 1024-10-1+1=1014*/

    int row=1;
    for(combination=1;combination<power(2,10);combination++){
        leftover = combination;
        help_sum=0;
        for(position=9;position>=0;position--){
            if(help_array[0][position]<=leftover){
                leftover -= help_array[0][position];
                help_array[row][position]=1;
                help_sum++;
            }
        }
        if(help_sum==1){
            for(position=9;position>=0;position--){
                help_array[row][position]=0;
            }
        }else{
            row++;
        }
    }

    while(go){
        number+=2;

        /*show progress*/
        if((number-1)%1000000==0){
            printf("%lld \n",number);
        }

        /*only continue if prime*/
        if(is_prime(number)){

            digits = f_count_digits(number);

            create_number_array(number,digits,pointer);

            /*count number of 0's, 1's, 2's (instances) excluding last digit*/
            for(search=0;search<=ten_min_goal;search++){
                instances=0;
                for(position=0;position<digits-1;position++){
                    if(number_array[position]==search){
                        instances++;
                    }
                }

                /*if 2 or more instances, continue*/
                if(instances>=2){

                    possibilities = power(2,instances);

                    /*create copy of array*/
                    for(position=0;position<digits;position++){
                        number_array_copy[position] = number_array[position];
                    }

                    /*loop through combinations and replace the instance with higher digits*/
                    for(combination=1;combination<=possibilities-instances-1;combination++){
                        /*lets say we replace 2's (search=2). we can assume that wrong is already 2 then. why? because if the combination with 0 and 1 are prime, we have already checked all combinations and it WAS NOT the number we are looking for. it's then incorrect to set wrong to search, but we save time. if they weren't prime, then setting wrong to 2 (search) is correct.*/
                        good=1;
                        wrong=search;
                        for(replacement=search+1;replacement<=9;replacement++){
                            help_position = 0;
                            for(position=0;position<digits;position++){
                                if(number_array[position]==search){

                                    /*instance found, now replace. if help array is 1, then replace with replacement, otherwise replace with search*/
                                    number_array_copy[position] = replacement*help_array[combination][help_position] + (1-help_array[combination][help_position])*search;

                                    help_position++;
                                }
                            }

                            /*verify if new number is prime. if more than 2 are not prime. try new combination*/
                            new_number = array_to_int(digits, number_array_copy);
                            if(is_prime(new_number)){
                                good++;
                                if(good==goal){
                                    printf("EUREKA! %lld",number);
                                    go=0;
                                    break;
                                }
                            }else{
                                wrong++;
                                if(wrong > ten_min_goal){
                                    break;
                                }
                            }
                        }
                    }
                }
            }
        }

        /*stop if above maximum*/
        if (number>100000000){
            go=0;
        }
    }
    return 0;
}
