# Valconeers Google Hash Code 2020

## TODO

- profile code
  - to see what code take much time 

- analytics
  - how many pictures
  - how many tags on average per picture
  - number of unique tags per problem
  - frequency of tags per problem


## extra todos 02/02/2022

- Is solved attribute
- Scorer toevoegen aan strategy
- Solve maken die een van solve, solve repeat en solve vector toepast
- N rep wordt attribute
- Vector solve maken
- Input data ook attribute maken en reset solution seed etc wanneer nieuwe imputdata

## extra todos 02/02/2022

- random seed ipv range zodat als we hem 2x runnen we een andere seed hebben

## Algorithms

1. First use a broad search
2. Thereafter use **Hill climbing**
   - can be used to make a good solution slightly better
     - if multiple improved solutions are found, then you can use those as new input
     - if __too many__ improved solutions are found, use a queue and prioritize the best scores first

More thoughts
- output should be perfectly reproducible. Currently, it is not entirely clear from the output filename how the output was created.