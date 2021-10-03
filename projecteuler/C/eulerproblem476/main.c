#include <stdio.h>
#include <stdlib.h>
#include <math.h>

double calc_radius(double a,double b, double c){
    double s = (a+b+c)/2.0;
    double T = sqrt(s*(s-a)*(s-b)*(s-c));
    return 2*T/(a+b+c);
}

int main()
{
    /* runs 220 seconds */
    /* because a<=b<=c largest circles cannot be in gamma corner*/
    double pi = 4.*atan(1.),alpha,beta,rdata[4]={0,0,0,0},max,totalA=0,nA=0,r1,A1;
    double ai,bi,ha2,aa2,ba2,ca2,hb2,ab2,bb2,cb2;
    double ha3,aa3,ba3,ca3,hb3,ab3,bb3,cb3;
    int n=1803,i,j,a,b,c,maxi;

    for(a=1;a<=n/2;a++){
        for(b=a;b<=n-a;b++){
            for(c=b;c<a+b;c++){

                /*radius largest circle*/
                r1 = calc_radius(a,b,c);
                /*area largest circle*/
                totalA += pi*r1*r1;

                /*opposite angles*/
                alpha = acos((b*b+c*c-a*a)/(2.0*b*c));
                beta = acos((a*a+c*c-b*b)/(2.0*a*c));

                /*length corner to center largest circle*/
                ai = r1/sin(0.5*alpha);
                bi = r1/sin(0.5*beta);

                /*calculate sides smaller triangle and radius*/
                ha2 = ai - r1;
                ba2 = ha2/sin(0.5*(pi-alpha));
                ca2 = ba2;
                aa2 = ba2*sin(alpha)/sin(0.5*(pi-alpha));
                rdata[0] = calc_radius(aa2,ba2,ca2);

                hb2 = bi - r1;
                ab2 = hb2/sin(0.5*(pi-beta));
                cb2 = ab2;
                bb2 = ab2*sin(beta)/sin(0.5*(pi-beta));
                rdata[1] = calc_radius(ab2,bb2,cb2);

                /*calculate smallest triangle in same corners as before*/
                ha3 = ha2 - 2*rdata[0];
                aa3 = aa2*ha3/ha2;
                ba3 = ba2*ha3/ha2;
                ca3 = ca2*ha3/ha2;
                rdata[2] = calc_radius(aa3,ba3,ca3);

                hb3 = hb2 - 2*rdata[1];
                ab3 = ab2*hb3/hb2;
                bb3 = bb2*hb3/hb2;
                cb3 = cb2*hb3/hb2;
                rdata[3] = calc_radius(ab3,bb3,cb3);

                /*use largest radii*/
                max = 0;
                for(j=1;j<=2;j++){
                    for(i=0;i<4;i++){
                        if(max<rdata[i]){
                            max = rdata[i];
                            maxi = i;
                        }
                    }
                    totalA += pi*max*max;
                    max = 0;
                    rdata[maxi] = 0;
                }
                nA++;
            }
        }
    }
    printf("answer: %1.5f",totalA/nA);
    return 0;
}
