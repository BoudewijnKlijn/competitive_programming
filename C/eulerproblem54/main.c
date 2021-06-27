#include <stdio.h>
#include <stdlib.h>

int main()
{
    FILE *fp;
    fp=fopen("C:\\Users\\BOUDEWIJN\\projecteuler-C\\eulerproblem54\\input.txt", "r");

    int x;
    long long i=0,j=0;

    int nieuw_spel = 1;
    while( (x = fgetc(fp)) != EOF){
        printf("%d",x);

        if(x=='\n'){
            printf("nieuw spel");
            nieuw_spel = 1;
            i++;
            return 1;
        }
        else if(x==' '){
            printf("nieuwe kaart");
            j++;
        }
    }
    fclose(fp);

    printf("%spel: %d,kaart: %d", i,j);
    return 0;
}
