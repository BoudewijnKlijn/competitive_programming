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

## 03-02-2022

Moeten we elke solution opslaan (met
Score, repr, hash van repr)?
Moet elke solution exact en snel reproduceerbaar zijn?

Ik denk allebei ja.

Als we elke solution opslaan dan kunnen we dat als input gebruiken voor ml oplossing Sebas (ook voor Gan idee Marco, en voor hillclimber)

Voor de hillclimber is het beter als de complete info van een solution snel reproduceerbaar is (voor dit probleem omdat je customers wilt toevoegen ipv ingrediënten, en customers worden niet opgeslagen in de output)

Als alles (snel) reproduceerbaar is kunnen we een hash van de repr van de strategie maken. Die hash is kort en kan bijvoorbeeld in de naam van de output. De hash mapt naar de settings.

Twee extra classes. Een Repeater en een Improver.

Repeater pakt strategie en voert meerdere keren uit, steeds met een andere seed. Strategieën zonder seed worden niet herhaald. Elke trial met een seed wordt opgeslagen.

Improver pakt een strategie (of output) voert die uit en past een (reproduceerbare?) verbetering toe.

Nog een idee: we kunnen direct met output genereren. Het is niet lastig om valide output te genereren. In het begin hebben we nog geen scorer, dus score weten we niet.  scorer zou dus moeten kunnen runnen op opgeslagen output. Zoveel mogelijk gebruikmaken van processing power van onze laptops. Er moet eigenlijk continue een oplossing worden uitgepoept


## 17-02-2022

- op welke probleem moeten we focussen. het probleem waar we nog de meeste punten kunnen winnen. we kunnen de theoretische max score berekenen, maar vaak is die niet te bereiken. we kunnen ook kijken hoe we het doen tov het leaderboard. maar dat is alleen mogelijk zolang het leaderboard openbaar is en wordt geupdatet.
- maak overzicht van interessante statistieken op basis van inputdata die kunnen worden gebruikt door strategies. bijv voor 2018, wat is de transitie (afstand) van ritje naar volgend ritje (dus van dropoff naar pickup). daarna moeten ritjes aan elkaar worden geregen door de laagste tranisitiescores te pakken.
