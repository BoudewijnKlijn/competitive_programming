clear all
close all
clc

tic

go = 1;
number = 0;

% 2520 omdat dat het kleinste getal is dat deelbaar is door 1 t/m 10.

while go == 1
    number = number + 2520;
    for i = 11 : 20
        if mod(number,i) == 0
            if i == 20
                go = 0;
                disp(number);
                break;
            end
        else
            break;
        end
    end
end

toc