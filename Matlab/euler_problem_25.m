close all
clear all
clc

fm = zeros(3,1000);
fm(1,1000) = 1;
fm(2,1000) = 1;
it = 2;

while fm(2,1) < 1
    it = it + 1;
    for col = 1000 : -1 : 1
        fm(3,col) = fm(2,col) + fm(1,col) + fm(3,col);
        if fm(3,col) > 9
            fm(3,col) = mod(fm(3,col),10);
            fm(3,col-1) = 1;
        end
    end
    fm(1,:) = [];
    fm(3,:) = zeros(1,1000);
end

disp(it)