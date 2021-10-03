close all
clear all
clc

% http://en.wikipedia.org/wiki/Permutation#Generation_in_lexicographic_order

n_cijfers = 10;
perm = 0:n_cijfers-1
it = 1;

while it < 1E6
    for k = n_cijfers-1 : -1 : 1
        if perm(1,k) < perm(1,k+1)
            l = find(perm(1,:)>perm(1,k),1,'last');
            it = it+1;
            c1 = perm(1,k);
            c2 = perm(1,l);
            perm(1,k) = c2;
            perm(1,l) = c1;
            
            perm_dummy = perm;
            % reverse order after k
            for i = k+1 : n_cijfers
                perm(1,i) = perm_dummy(1,n_cijfers+k+1-i);
            end
%             disp(perm)
            break;
        end
    end
end
disp(perm)