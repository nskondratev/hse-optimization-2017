# HSE 2017. Optimization
## Lab 1 - Local Search Methods
### Task
Implement:
- [x] Repeated Local Search
- [x] Iterated Local Search
- [x] Guided Local Search

for [Quadratic Assignment Problem](https://en.wikipedia.org/wiki/Quadratic_assignment_problem).

### Test instances
Test instances are placed in directory *./lab_1/test_instances/*.

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

# Lab 2 - Variable Neighborhood Search
### Task
Implement General VNS Scheme for the Cell Formation Problem (Biclustering).

### Test instances
Test instances are placed in directory ./lab_2/test_instances/

### Input format
m p (number of machines and parts)

*Next m rows:*

m(row number) list of parts processed by machine m separated by space

e.g:

1 9 17 19 31 33

means machine 1 processes parts 9 17 19 31 33

### Output format
#### Filename
*instancename*.sol (e.g. **20x20.sol**)
#### Format
*m1_clusterId m2_clusterId ...*  - machines to clusters mapping

*p1_clusterId p2_clusterId ...*  - parts to clusters mapping

### Running
#### Prerequisites
* Python 3
* Installed packages: *numpy*

#### How to run
* Go to *lab_2* directory
* Run *main.py* with the desirable log level (default log level: INFO)

Example:
```bash
$ LOG_LEVEL=DEBUG python3 main.py
```
