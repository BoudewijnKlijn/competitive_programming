close all
clear all
clc
format compact

tic

i = 0;
tri = 0;
go = 1;

while go == 1
    i = i + 1;
    tri = tri + i;
    count_div = 0;
    sqrt_tri = sqrt(tri);
    for j = 1 : sqrt_tri;
        if mod(tri,j) == 0
            if j ~= sqrt_tri
                count_div = count_div + 2;
            else
                count_div = count_div + 1;
            end
        end
    end
    if count_div > 500
        go = 0;
    end
end
disp(tri)

toc