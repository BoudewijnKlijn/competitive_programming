clear all
clc
% zeef van Eratosthenes

max_number = 2E6;
sqrt_max_number = sqrt(max_number);

i = 1;
all = (2:max_number)';

while all(i,1) < sqrt_max_number
    multiples = (all(i,1)^2 : all(i,1) : max_number)';
    all = setdiff(all,multiples);
    i = i + 1;
end

format longg
disp(sum(all));