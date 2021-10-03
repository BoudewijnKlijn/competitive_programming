clear all

fibo(1,1) = 1;
fibo(2,1) = 2;

som = 2;

while fibo(end,1) < 4E6
    fibo(end+1,1) = fibo(end,1) + fibo(end-1,1);
    if fibo(end,1) < 4E6 && mod(fibo(end,1),2) == 0
        som = som + fibo(end,1);
    end
end

disp(som)
