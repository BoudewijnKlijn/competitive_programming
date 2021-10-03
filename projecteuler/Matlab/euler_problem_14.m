close all
clear all
clc

tic

matrix = zeros(1E6-1,2);
matrix(1,:) = [1,1];

for i = 2 : 1E6-1
    number = i;
    matrix(i,1) = i;
    chain = 0;
    while number ~= 1 && number > i-1
        chain = chain + 1;
        if mod(number,2) == 0
            number = number / 2;
        else
            number = number*3 + 1;
        end
    end
    
    if number < i
        matrix(i,2) = chain + matrix(number,2);
    else
        matrix(i,2) = chain;
    end
end

disp(find(matrix(:,2)==max(matrix(:,2))))

toc