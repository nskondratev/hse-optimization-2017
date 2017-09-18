# HSE 2017. Optimization
## Lab 1 - Local Search Methods
### Task
Implement:
- [ ] Repeated Local Search
- [ ] Iterated Local Search
- [ ] Guided Local Search

for [Quadratic Assignment Problem](https://en.wikipedia.org/wiki/Quadratic_assignment_problem).

### Test instances
Test instances are placed in directory *./lab-1/test_instances/*.

### Input format
n (number of plants/locations)

*Next n rows*: distances matrix D

*Empty row*

*Next n rows*: flows matrix F

### Output file
#### Filename
*instancename*.sol (e.g. **Tai20a.sol**)
#### Format
*a1 a2 a3 ... an* - solution (permutation means plant a1 is opened in location 1 and so on, separator - spacebar)
