%eulerproblem 551
page_output_immediately (1);
more off;

pkg load io;
pkg load windows;

tic

options = 100;
previous = 1;

options_extra = zeros(options+1,options+1);

extra_table = zeros(options,2);
extra_table(1,2)=1;
for i=1:options
  options_extra(i+1,1) = i;
  options_extra(1,i+1) = i;
  extra_table(i,1) = i;
endfor

max_x = 300000;
first_x_after_1 = zeros(max_x,30);
for i=1:max_x
  first_x_after_1(i,1) = i;
endfor

x=1;
col = 1;
range = 0;

a_n = 1;
n = 1; 

for n=1:333000
  extra = sum_digits(a_n);
  extra_table(extra,2)+=1;
  
  if(x<max_x)
    %if(mod(x-1,65536)==0)
      %range += 65536;
      %col++;
    %endif
    first_x_after_1(x-range,3*(col-1)+1) = n;
    first_x_after_1(x-range,3*(col-1)+2) = a_n;
    first_x_after_1(x-range,3*(col-1)+3) = extra;
    x++;
  endif
   
  if(extra == 4)
    x = 1;
    col++;
    
    previous
    n
    a_n
    extra
  endif
  
  if(options_extra(previous+1,extra+1)==0)
    previous;
    n;
    a_n;
    extra;
  endif
  
  a_n += extra;

  options_extra(previous+1,extra+1)++;
  previous = extra;
endfor

toc

xlswrite ('test2.xlsx', first_x_after_1)