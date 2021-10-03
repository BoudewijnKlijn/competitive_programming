clear all

go = 1;
number = 999*999;

while go == 1;
    number = number - 1;
    string = num2str(number);
    if string(1) == string(end) && string(2) == string(end-1) && string(3) == string(end-2)
        for i = 999 : -1 : 101
            if mod(number,i) == 0;
                if number/i > 99 && number/i < 1000
                    go = 0;
                    disp(i)
                    disp(number/i)
                    break;
                end
            end
        end
    end
end