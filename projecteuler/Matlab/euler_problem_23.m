clear all
close all
clc

matrix = zeros(10000,1);

for number = 2 : 28123
    sqrt_number = sqrt(number);
    sum_div = 0;
    for div = 1 : sqrt_number
        if mod(number,div) == 0
            if div == sqrt_number || div == 1
                sum_div = sum_div + div;
            else
                sum_div = sum_div + number/div + div;
            end
        end
    end
    matrix(number,1) = sum_div;
end

% collect abundant numbers
count = 0;
row = 0;
while row < 28123
    row = row + 1;
    if matrix(row,1) > row
        count = count + 1;
        abundant_matrix(count,1) = row;
    end
end

sum_two = zeros(size(abundant_matrix,1),size(abundant_matrix,1));
for i = 1 : length(abundant_matrix)
    for j = 1 : length(abundant_matrix)
        sum_two(i,j) = abundant_matrix(i,1) + abundant_matrix(j,1);
    end
end
uniek = unique(sum_two);
set_of_all = (1:28123)';

disp(sum(setdiff(set_of_all,uniek))) % som getallen die wel in set_of_all zitten en niet in uniek