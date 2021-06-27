clear all
close all
clc

tic

number = 600851475143;

prime_vector = primes(10000)';

prime_factors = 1;

while number ~= 1
    for i = 1 : size(prime_vector,1)
        if mod(number,prime_vector(i,1)) == 0
            prime_factors(end+1,1) = prime_vector(i,1);
            number = number/prime_vector(i,1);
            break;
        end
    end
end

disp(prime_factors(end,1))

toc