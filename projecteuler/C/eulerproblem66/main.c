#include <stdio.h>
#include <stdlib.h>

int get_floor(int b, int a2, int a1, int a02D){
    while((b+1)*(b+1)*a2*a2+a1*a1-2*a1*(b+1)*a2 < a02D){
        b++;
    }
    return b;
}

int verify_old(int x, int y, int D){
    return (x*x - D*y*y==1);
}

int verify(int * x, int * y, int D, int max_col){
    int dummy, remainder_x=0, remainder_y=0, i, j, array_x[200]={}, array_y[200]={};

    /*create x^2 and y^2 in array form*/
    for(i=max_col;i>max_col/2;i--){
        for(j=max_col;j>max_col/2;j--){
            dummy = x[i]*x[j] + remainder_x + array_x[i+j-max_col];
            array_x[i+j-max_col] = dummy%10;
            remainder_x = dummy/10;

            dummy = y[i]*y[j] + remainder_y + array_y[i+j-max_col];
            array_y[i+j-max_col] = dummy%10;
            remainder_y = dummy/10;
        }
    }

    /*calculate D*y^2 +1*/
    for(i=max_col;i>=0;i--){
        if(i==max_col){
            remainder_y=1;/*add the +1 from the right side */
        }
        dummy = array_y[i]*D + remainder_y;
        array_y[i] = dummy%10;
        remainder_y = dummy/10;
    }

    /*compare x^2 with D*y^2+1, if both arrays are equal => solution found*/
    for(i=max_col;i>=0;i--){
        if(array_y[i]!=array_x[i]){
            return 0; /*not found*/
        }
    }
    return 1; /*found*/
}

int f_gcd(int a, int b, int c){
    int div=2, total=1;
    while(div<=a && div<=b && div<=c){
        if(a%div==0 && b%div==0 && c%div==0){
            total = total*div;
            a = a/div;
            b = b/div;
            c = c/div;
        }else{
            div++;
        }
    }
    return total;
}

/*answer: 661, runs in 1.7s*/
int main()
{
    /*Continued fractions play an essential role in the solution of Pell's equation. For example, for positive integers p and q,
    and non-square n, it is true that p2 − nq2 = ±1 if and only if p / q is a convergent of the regular continued fraction for √n.
    https://en.wikipedia.org/wiki/Continued_fraction
    https://math.stackexchange.com/questions/783521/solving-pells-equation-algorithm-to-converge-sqrt-n
    https://en.wikipedia.org/wiki/Pell%27s_equation
    https://math.stackexchange.com/questions/171803/how-to-solve-this-pells-equation-x2-991y2-1?rq=1
    */

    int D, b[1000]={},a0[1000]={},a1[1000]={},a2[1000]={}, h_old[1002]={}, k_old[1002]={}, h[1002][200]={}, k[1002][200]={}, gcd, found=0, i, j, m;
    int remainder_h, remainder_k, dummy, col, largest[200]={}, max_col=199, largest_D=0;
    for(D=1;D<=1000;D++){

        h[0][max_col]=0; /*represents h[-2]*/
        h[1][max_col]=1; /*represents h[-1]*/
        k[0][max_col]=1; /*represents k[-2]*/
        k[1][max_col]=0; /*represents k[-1]*/

        /*h_old[0]=0;
        h_old[1]=1;
        k_old[0]=1;
        k_old[1]=0;*/

        a0[0]=1;
        a1[0]=0;
        a2[0]=1;

        found = 0;
        i=0;
        while(!found){
            b[i] = get_floor(0,a2[i],a1[i],a0[i]*a0[i]*D);

            /*h_old[i+2] = h_old[i+1]*b[i] + h_old[i];
            k_old[i+2] = k_old[i+1]*b[i] + k_old[i];
            verify_old(h_old[i+2], k_old[i+2], D);*/

            /*calculate h and k in array form*/
            remainder_h = 0;
            remainder_k = 0;
            for(col=max_col;col>=0;col--){
                dummy = h[i+1][col]*b[i] + h[i][col] + remainder_h;
                h[i+2][col] = dummy%10;
                remainder_h = dummy/10;
                dummy = k[i+1][col]*b[i] + k[i][col] + remainder_k;
                k[i+2][col] = dummy%10;
                remainder_k = dummy/10;
            }

            /*verify if answer is correct. store if largest*/
            if (verify(h[i+2], k[i+2], D, max_col)){
                found=1;
                for(j=0;j<=max_col;j++){
                    if(largest[j]>h[i+2][j]){
                        break;
                    }else if(h[i+2][j]>largest[j]){
                        largest_D = D;
                        for(m=0;m<=max_col;m++){
                            largest[m]=h[i+2][m];
                        }
                        break;
                    }
                }
                break;
            }

            a0[i+1]= a2[i]*a0[i];
            a1[i+1]= -a2[i]*(a1[i]-b[i]*a2[i]);
            a2[i+1]= a0[i]*a0[i]*D-(a1[i]-b[i]*a2[i])*(a1[i]-b[i]*a2[i]);

            /*numbers will get really big, so divide by greatest common divisor*/
            gcd = f_gcd(a0[i+1],a1[i+1],a2[i+1]);
            if(gcd>1){
                a0[i+1]= a0[i+1]/gcd;
                a1[i+1]= a1[i+1]/gcd;
                a2[i+1]= a2[i+1]/gcd;
            }

            i++;
        }
    }

    /*print solution*/
    printf("Largest x:");
    for(j=0;j<=max_col;j++){
        printf("%d",largest[j]);
    }
    printf(", D:%d",largest_D);
    return 0;
}
