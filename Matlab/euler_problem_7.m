clear all

go = 1;
limit = 10001;
primes = zeros(limit,1);
primes(1,1) = 2;
n_primes = 1;
i = 2;

while n_primes < limit
    i = i + 1;
%     if mod(i,10000) == 0;
%         n_primes
%     end
    for j = 1 : n_primes
        if mod(i,primes(j,1)) == 0;
            break;
        elseif mod(i,primes(j,1)) ~= 0 && j == n_primes
            primes(n_primes+1,1) = i;
            n_primes = n_primes + 1;
        end
    end
end
