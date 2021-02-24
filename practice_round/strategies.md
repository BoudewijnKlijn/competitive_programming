# Strategies

Sum of squares of unique ingredients per team. 

Combining pizzas with __many__ and __non-overlapping ingredients__ will result in a high score.

## input B

- Only 10 unique ingredients. 
    - Some pizzas contain all of them.
- 500 pizzas and 550 teams  

## general strategies

- valid solution
- shuffle and make valid
- order and make valid solutions
- valid solution and pick best orders, repeat

Valid
Multiple
Better sort
Simultaan vooruit combineren van 10 ofzo en de beste houden

Func voor teams
Func voor order pizzas

maak random orders. gooi de slechtste (x of x% weg). bewaar de beste (overig). herhaal met resterende data.

splits data in brokken. bepaal optimale oplossing voor gegeven data. (kan gebruikt worden voor kleinere dataset, bijvoorbeeld laatst 5-10% van input set.) combineer daarna met oplossing voor andere subsets. let op data combineren wel kan! (kan mogelijk niet door constraints) 
