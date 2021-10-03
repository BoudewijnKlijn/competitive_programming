clear all
clc

a = (1:1000)';
asq = a.^2;
b = (1:1000)';
bsq = b.^2;
c = (1:1000)';
csq = c.^2;

for ia = 1 : 1000
    for ib = 1 : 1000
        for ic = 1 : 1000
            if asq(ia,1) + bsq(ib,1) == csq(ic,1)
                if ia+ib+ic == 1000
                    disp(ia*ib*ic)
                    break;
                end
            end
        end
    end
end