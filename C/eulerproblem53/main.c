#include <stdio.h>
#include <stdlib.h>

int main()
{
    int num_array[200]={}, denom_array[200]={}, max_pos = 199, pos, first_pos_num, first_pos_denom;
    int n, r, gt1m=0, remainder, multi,dummy;

    for(n=23;n<=100;n++){
        for(r=1;r<=n;r++){

            /*reset arrays to zero*/
            for(pos=0;pos<=max_pos;pos++){
                num_array[pos]=0;
                denom_array[pos]=0;
            }

            /*create numerator*/
            num_array[max_pos] = 1;
            remainder = 0;
            for(multi=2;multi<=n;multi++){
                for(pos=max_pos;pos>=0;pos--){
                    dummy = num_array[pos]*multi+remainder;
                    remainder=dummy/10;
                    num_array[pos]=dummy%10;
                }
            }

            /*create denominator*/
            denom_array[max_pos] = 1;
            remainder = 0;
            for(multi=2;multi<=r;multi++){
                for(pos=max_pos;pos>=0;pos--){
                    dummy = denom_array[pos]*multi+remainder;
                    remainder=dummy/10;
                    denom_array[pos]=dummy%10;
                }
            }
            for(multi=2;multi<=n-r;multi++){
                for(pos=max_pos;pos>=0;pos--){
                    dummy = denom_array[pos]*multi+remainder;
                    remainder=dummy/10;
                    denom_array[pos]=dummy%10;
                }
            }

            /*difference*/
            first_pos_num=0;
            first_pos_denom=0;
            for(pos=0;pos<=max_pos;pos++){
                if(first_pos_num==0 && num_array[pos]!=0){
                    first_pos_num = pos;
                }
                if(first_pos_denom==0 && denom_array[pos]!=0){
                    first_pos_denom = pos;
                }
            }

            if(first_pos_denom-first_pos_num>6){
                gt1m++;
            }
            else if(first_pos_denom-first_pos_num==6){
                for(pos=first_pos_num;pos<=max_pos-6;pos++){
                    if(num_array[pos]>denom_array[pos+6]){
                        gt1m++;
                        break;

                    }else if(num_array[pos]<denom_array[pos+6]){
                        break;
                    }
                }
            }
        }
    }

    printf("\n# greater than 1 million: %d\n",gt1m);
    return 0;
}
