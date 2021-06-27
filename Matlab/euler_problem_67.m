% ok gewoon van onder naar boven werken.
% je hebt steeds twee opties om van boven naar beneden te gaan. tel het
% hoogste getal van de twee opties onderste rij op bij de rij erboven, en werk omhoog.

close all
clear all
clc
format compact

data = xlsread('euler_problem_67.xlsx');

N = size(data,1);

for row = N : -1 : 2
    for col = 1 : row-1
        if data(row,col) > data(row,col+1)
            data(row-1,col) = data(row-1,col) + data(row,col);
        else
            data(row-1,col) = data(row-1,col) + data(row,col+1);
        end
    end
end

disp(data(1,1));