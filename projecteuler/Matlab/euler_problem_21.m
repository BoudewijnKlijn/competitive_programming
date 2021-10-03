clear all
close all
clc

matrix = zeros(10000,1); % sum proper divisors

for number = 2 : 10E3
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

sum_amicable_numbers = 0;
for i = 1 : 10E3
    if matrix(i,1) ~= 0 && matrix(i,1) ~= i && matrix(i,1) < 10000
        if matrix(matrix(i,1),1) == i
            sum_amicable_numbers = sum_amicable_numbers + i + matrix(i,1);
            matrix(matrix(i,1),1) = 0;
            matrix(i,1) = 0;
        end
    end
end
disp(sum_amicable_numbers);