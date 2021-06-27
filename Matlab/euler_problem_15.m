% kan waarschijnlijk ook met permutaties,faculteit etc.
close all
clear all
clc
format longg

tic

grid = 20;

matrix = zeros(grid+1,grid+1);
matrix(grid+1,:) = ones(grid+1,1);
matrix(:,grid+1) = ones(1,grid+1);

for row = grid : -1 : 1
    for col = grid : -1 : 1
        matrix(row,col) = matrix(row+1,col) + matrix(row,col+1);
    end
end

disp(matrix(1,1))   

toc