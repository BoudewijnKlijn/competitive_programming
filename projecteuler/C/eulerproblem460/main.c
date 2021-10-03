#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <limits.h>

double time(int x0,int y0,int x1,int y1){
    double s = sqrt((x1-x0)*(x1-x0) + (y1-y0)*(y1-y0));
    double v = y0;
    if(y0!=y1){
        v = (y1-y0)/(log(y1)-log(y0));
    }
    return s/v;
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

int** Make2DIntArray(int arraySizeX, int arraySizeY) {
    int** theArray;
    int i;
    theArray = (int**) malloc(arraySizeX*sizeof(int*));
    for (i = 0; i < arraySizeX; i++){
       theArray[i] = (int*) malloc(arraySizeY*sizeof(int));
    }
    return theArray;
}


int main()
{
    /*Analyse 0: probleem is symmetrisch dus alleen eerste helft oplossen*/
    /*Analyse 1: snelheid horizontaal is altijd groter dan of gelijk aan snelheid verticaal of diagonaal, met dezelfde eindhoogte y1.*/
    /*Analyse 1.1: laatste stukje van x:d/2-1n naar x:d/2 moet je horizontaal afleggen.*/
    /*Analyse 2: (triviaal) afstand diagonaal (h omhoog en s+1 opzij) is korter dan diagonal (h omhoog en 1 opzij) + horizontaal (s opzij).
                    echter de snelheid is net iets lager. het is me nog onduidelijk of de kortere afstand opweegt tegen de gemiddeld lagere snelheid */
    /*Analyse 3: omdat we slechts de helft van het problem bekijken, moet je NOOIT omlaag gaan. ALLE beste mogelijkheden liggen tussen loodrecht omhoog en horizontaal opzij. */
    /*Analyse 4: op hoogte y0, eerst diagonaal 1 omhoog en opzij en daarna 1 opzij, of in een keer diagonaal 1 omhoog en 2 opzij. LAATSTE wanneer y0>1.
                    optie 1: sqrt(2)*log(1/(y0+1)) + 1/(y0+1)
                    optie 2: sqrt(5)*log((y0+1)/y0) */
    /*Analyse 4.1: sterkere versie van 4. voor diagonaal h omhoog en 1 opzij en daarna nog eens 1 opzij, of diagonaal h omhoog en 2 opzij in 1 keer.
                    optie 1: sqrt(h^2+1)/h * ln((y0+h/y) + 1/(y0+h)
                    optie 2: sqrt(h^2+2^2)/h * ln((y0+h/y)
                    --> in limiet h/(y0+h) <= ln((y0+h)/y0) -->
                    en dus: sqrt(h^2+4) - sqrt(h^2+1) < 1/(y0+h) (LET OP, dit geldt dus pas voor grote y0, even uitzoeken vanaf welke combinaties van y0 en h.)
                                                  */
    /*Analyse 5: van links naar rechts bekeken, wordt de helling van een nieuw lijnstuk steeds vlakker. omgekeerd kunnen we dus beredeneren, dat vanaf rechts naar links steeds steiler wordt
    daarom: als je op een bepaalde hoogte begint. en je moet naar punt (0,1), dan kan je een hele onderste driehoek uitsluiten. je kan daar namelijk nooit komen, want het eerste lijnstuk is horizontaal
    naar links, en daarna wordt het steeds steiler.*/


    double** time_matrix = Make2DDoubleArray(5001,5001); /*second argument = d/2+1*/
    int** destX_matrix = Make2DIntArray(5001,5001); /*second argument = d/2+1*/
    int** destY_matrix = Make2DIntArray(5001,5001); /*second argument = d/2+1*/
    int d=10000,x,y,destX,destY,ylimit=5001;

    /*set time halfway to zero. destinations horizontal*/
    x = d/2;
    for(y=1;y<ylimit;y++){
        time_matrix[y][x] = 0;
        destX_matrix[y][x] = x+1;
        destY_matrix[y][x] = y;
    }
    /*set time halfway-1 to distance/horizontal speed and destinations horizontal*/
    x = d/2-1;
    for(y=2;y<ylimit;y++){
        time_matrix[y][x] = 1.0/y;
        destX_matrix[y][x] = x+1;
        destY_matrix[y][x] = y;
    }
    /*one exception for y==1*/
    time_matrix[1][d/2-1] = sqrt(2.0)*log(2);
    destX_matrix[1][d/2-1] = d/2;
    destY_matrix[1][d/2-1] = 2;

    /*set upper destinations of limit horizontal for upper row of destination matrices*/
    y=ylimit-1;
    for(x=d/2-1;x>=0;x--){
        time_matrix[y][x] = (d/2.0-x)/y;
        destX_matrix[y][x] = x+1;
        destY_matrix[y][x] = y;
    }

    double upper_bound,lower_bound;

    for(x=(d/2)-2;x>=0;x--){
        printf("x=%d\n",x);

        for(y=ylimit-2;y>0;y--){
            /*upper bound angle set by point above. if upper bound is zero, then new angle must be zero too.*/
            /*if(destX_matrix[y+1][x]!=x){
                upper_bound = 1.0*(destY_matrix[y+1][x]-(y+1))/(destX_matrix[y+1][x]-x);
            }
            else{
                upper_bound = -1;
            }*/
            /*lower bound angle set by point to the right, if lower bound is unlimited than new angle must be unlimited too.*/
            /*if(destX_matrix[y][x+1]!=x+1){
                lower_bound = 1.0*(destY_matrix[y][x+1]-y)/(destX_matrix[y][x+1]-x-1);
            }
            else{
                lower_bound  = -1;
            }*/
            /*printf("upper:%f,lower:%f\n",upper_bound,lower_bound);*/

            time_matrix[y][x] = (d/2.0-x)/y;
            destX_matrix[y][x] = x+1;
            destY_matrix[y][x] = y;


            for(destX=x;destX<=d/2;destX++){
                for(destY=y;destY<ylimit;destY++){
                    if( (time(x,y,destX,destY) + time_matrix[destY][destX]) <= time_matrix[y][x]){
                        time_matrix[y][x] = time(x,y,destX,destY) + time_matrix[destY][destX];
                        destX_matrix[y][x] = destX;
                        destY_matrix[y][x] = destY;
                    }
                }
            }

            /*if( destX_matrix[y][x]==x ){
                /*printf("error. goes straight up. x=%d,y=%d\n",x,y);
            }*/

            /*if(upper_bound>1){
                if( 1.0*(destY_matrix[y][x]-y)/(destX_matrix[y][x]-x) > 1.0+upper_bound){
                    printf("upper\n");
                }
            }
            else if( 1.0*(destY_matrix[y][x]-y)/(destX_matrix[y][x]-x) > 2.0*upper_bound){
                    printf("upper\n");
            }*/

            /*if( 1.0*(destY_matrix[y][x]-y)/(destX_matrix[y][x]-x) > upper_bound){
                printf("upper\n");

            }*/
            /*if( destY_matrix[y][x] > destY_matrix[y+1][x]){
                printf("upper\n");
                printf("new: (%2d,%2d)->(%2d,%2d) old: (%2d,%2d)->(%2d,%2d), ang=%f\n",x,y,destX_matrix[y][x],destY_matrix[y][x],x,y+1,destX_matrix[y][x],destY_matrix[y+1][x],1.0*(destY_matrix[y][x]-y)/(destX_matrix[y][x]-x));
                printf("y %d, y+1 %d\n",destY_matrix[y][x],destY_matrix[y+1][x]);

            }*/
            /*if(1.0*(destY_matrix[y][x]-y)/(destX_matrix[y][x]-x) < 1.0*lower_bound ){
                printf("lower\n");
                printf("new: (%2d,%2d)-(%2d,%2d) old: (%2d,%2d)-(%2d,%2d), ang=%f\n",x,y,destX_matrix[y][x],destY_matrix[y][x],x+1,y,destX_matrix[y][x+1],destY_matrix[y][x+1],1.0*(destY_matrix[y][x]-y)/(destX_matrix[y][x]-x));
                getchar();
                printf("(%2d,%2d) to (%2d,%2d), lb = %f, angle = %f, ub=%f\n",x,y,destX_matrix[y][x],destY_matrix[y][x],lower_bound,1.0*(destY_matrix[y][x]-y)/(destX_matrix[y][x]-x),upper_bound);
            }*/


        }
    }
    printf("\n\nbest time: %.9f\n",2*time_matrix[1][0]);
    return 0;
}

    /*printf("\n\n");
    for(y=ylimit-1;y>=0;y--){
        for(x=0;x<=d/2;x++){
            if(y>0){
                printf("(%2d,%2d)",destX_matrix[y][x],destY_matrix[y][x]);
            }
            else{
                printf("(x =%2d)",x);
            }
        }
        printf("\n");
    }*/

/*

    /*int y0=2,h;
    double new_time,old_time = 0,new_diff,old_diff = 0;;
    for(h=1;h<10;h++){
        new_time = sqrt(h*h+1)/h * (log(y0+h)-log(y0)) + 1/(y0+h);
        printf("%.8f,",new_time);
        new_diff = new_time-old_time;
        if(new_diff>old_diff){
            printf("ooooo,");
        }
        else{
            printf("iiiii,");
        }
        old_diff = new_diff;
        if(new_diff>0){
            printf("+++\n");
        }
        else{
            printf("---\n");
        }

        old_time = new_time;
    }
    printf("\n\n");




double space(long long x0,long long y0,long long x1,long long y1){
    return sqrt((x1-x0)*(x1-x0) + (y1-y0)*(y1-y0));
}

double speed(long long y0, long long y1){
    if(y0==y1){
        return y0;
    }
    return (y1-y0)/(log(y1)-log(y0));
}
    maxi = 1+exp(d/2);
    if(maxi<0){
        maxi = 1000000000;
    }
    printf("maxi: %lld\n",maxi);
    for(i=1;i<maxi;i++){
        for(dx1=0;dx1<=d;dx1++){
            for(dx2=d-dx1;dx2>=0;dx2--){
                new_time = 1.0*time(0,1,dx1,i)+1.0*time(dx1,i,d-dx2,i)+1.0*time(d-dx2,i,d,1);
                if(new_time<best_time){
                    best_time = new_time;
                    best_dx1 = dx1;
                    best_dx2 = dx2;
                }
            }
        }
    }

    printf("d=%d,dx1=%d,dx2=%d\n",d,best_dx1,best_dx2);
    printf("best time: %.9f\n",best_time);
*/
