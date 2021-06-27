close all
clear all
clc

matrix = zeros(1,310);
matrix(1,end) = 2;

for i = 2 : 1000
    for j = 1 : length(matrix)
        number = matrix(1,j) * 2;
        if number > 9
            matrix(1,j) = mod(number,10);
            matrix(1,j-1) = matrix(1,j-1) + 1;
        else
            matrix(1,j) = number;
        end
    end
end
disp(sum(matrix))