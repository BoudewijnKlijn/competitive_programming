
from assignment import read_assignment

assignment = read_assignment("b_little_bit_of_everything.in")

print(assignment)
print(assignment.n_teams_four + assignment.n_teams_three + assignment.n_teams_two)
print(assignment.n_teams_four*4 + assignment.n_teams_three*3 + assignment.n_teams_two*2)

print(assignment.pizzas)

unique = set()
for pizza in assignment.pizzas:
    unique.update(pizza.ingredients)
print(unique)
