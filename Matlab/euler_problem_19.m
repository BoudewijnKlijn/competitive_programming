clear all
close all
clc

matrix = zeros(36891,4);
nthday = 0;

for year = 1900 : 2000
    for month = 1 : 12
        if month == 4 || month == 6 || month == 9 || month == 11
            max_day = 30;
        elseif month == 2
            max_day = 28;
            if mod(year,4) == 0
                max_day = 29;
                if mod(year,100) == 0
                    max_day = 28;
                       if mod(year,400) == 0
                            max_day = 29;
                       end
                end
            end
        else
            max_day = 31;
        end
        for day = 1 : max_day
            nthday = nthday + 1;
            sortofday = mod(nthday,7);
            matrix(nthday,:) = [year,month,day,sortofday];
        end
    end
end

som = 0;
for i = 367 : 36891
    if matrix(i,3) == 1 && matrix(i,4) == 0
        som = som + 1;
    end
end

disp(som)