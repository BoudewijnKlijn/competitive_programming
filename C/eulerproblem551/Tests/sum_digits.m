function [sum] = sum_digits (number)
  
  sum = 0;
  while(number>0)
    sum = sum + mod(number,10);
    number = floor(number/10);
  endwhile
  
endfunction
