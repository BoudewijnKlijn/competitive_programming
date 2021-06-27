% gerelateerd aan 16.

close all
clear all
clc

matrix = zeros(1,160);
matrix(1,end) = 1;

for i = 2 : 10
    for j = 1 : length(matrix)
        number = matrix(1,j) * i;
        if number > 99
            matrix(1,j-2) = matrix(1,j-2) + (number-mod(number,100))/100;
            number = mod(number,100);
        end
        if number > 9
            matrix(1,j-1) = matrix(1,j-1) + (number-mod(number,10))/10;
            number = mod(number,10);
        end
        matrix(1,j) = number;
        for jj = length(matrix) : -1 : 1
            if matrix(1,jj) > 9
                matrix(1,jj-1) = matrix(1,jj-1) + (matrix(1,jj)-mod(matrix(1,jj),10))/10;
                matrix(1,jj) = mod(matrix(1,jj),10);
            end
        end    
    end
end
disp(sum(matrix))