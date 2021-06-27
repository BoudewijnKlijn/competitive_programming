#include <stdio.h>
#include <stdlib.h>

int main()
{
    int i1,i2,i3,i4,i5,i6,i7,i8;
    int v1,v2,v3,v4,v5,v6,v7,v8;
    int sum;

    v1 = 200;
    v2 = 100;
    v3 = 50;
    v4 = 20;
    v5 = 10;
    v6 = 5;
    v7 = 2;
    v8 = 1;

    int x = 0;
    for(i1=0;i1<=200/v1;i1++){
        sum = i1*v1;
        if(sum==200){
            x++;
            continue;
        }else if(sum>200){break;}
        for(i2=0;i2<=200/v2;i2++){
            sum = i1*v1 + i2*v2;
            if(sum==200){
                x++;
                continue;
            }else if(sum>200){break;}
            for(i3=0;i3<=200/v3;i3++){
                sum = i1*v1 + i2*v2+i3*v3;
                if(sum==200){
                    x++;
                    continue;
                }else if(sum>200){break;}
                for(i4=0;i4<=200/v4;i4++){
                    sum = i1*v1 + i2*v2+i3*v3+i4*v4;
                    if(sum==200){
                        x++;
                        continue;
                    }else if(sum>200){break;}
                    for(i5=0;i5<=200/v5;i5++){
                        sum = i1*v1 + i2*v2+i3*v3+i4*v4+i5*v5;
                        if(sum==200){
                            x++;
                            continue;
                        }else if(sum>200){break;}
                        for(i6=0;i6<=200/v6;i6++){
                        sum = i1*v1 + i2*v2+i3*v3+i4*v4+i5*v5+i6*v6;
                            if(sum==200){
                                x++;
                                continue;
                            }else if(sum>200){break;}
                            for(i7=0;i7<=200/v7;i7++){
                                sum = i1*v1 + i2*v2+i3*v3+i4*v4+i5*v5+i6*v6+i7*v7;
                                if(sum==200){
                                    x++;
                                    continue;
                                }else if(sum>200){break;}
                                for(i8=0;i8<=200/v8;i8++){
                                    sum = i1*v1 + i2*v2+i3*v3+i4*v4+i5*v5+i6*v6+i7*v7+i8*v8;
                                    if(sum==200){
                                        x++;
                                        continue;
                                    }else if(sum>200){break;}
                                }
                            }
                        }
                    }
                }
            }
        }
    }
    printf("answer: %d",x);
    return 0;
}
