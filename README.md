# Z8000 RISC CPU simulator
This simulator prints the state of the memory and registers for each CPU cycle of the execution of a program.

## Supported instructions
- `LOAD register address` Loads a value from the memory to a register 
- `STORE address register` Writes a value from a register to the memory 
- `MOVE destination source` Moves a value from a register to another 
- `MVC destination constant` Moves a constant value to a register 
- `IADD destination source` Adds two values
- `IMUL destination source` Multiplues two values

## Usage
`python simulator.py`

Execution example:
```
python simulator.py
test_prog.txt

Cycle:
1
Pipeline 1:
[0, -1, -1, -1, -1]
Pipeline 2:
[1, -1, -1, -1, -1]
Registers:
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
Memory:
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

Cycle:
2
Pipeline 1:
[2, 0, -1, -1, -1]
Pipeline 2:
[3, 1, -1, -1, -1]
Registers:
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
Memory:
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

Cycle:
3
Pipeline 1:
[-1, 2, 0, -1, -1]
Pipeline 2:
[-1, 3, 1, -1, -1]
Registers:
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
Memory:
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

Cycle:
4
Pipeline 1:
[-1, 2, -1, 0, -1]
Pipeline 2:
[-1, 3, -1, 1, -1]
Registers:
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
Memory:
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

Cycle:
5
Pipeline 1:
[-1, 2, -1, -1, 0]
Pipeline 2:
[-1, 3, -1, -1, 1]
Registers:
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
Memory:
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

Cycle:
6
Pipeline 1:
[-1, -1, 2, -1, -1]
Pipeline 2:
[-1, 3, -1, -1, -1]
Registers:
[0, 10, 4, 0, 0, 0, 0, 0, 0, 0]
Memory:
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

Cycle:
7
Pipeline 1:
[-1, -1, 2, -1, -1]
Pipeline 2:
[-1, 3, -1, -1, -1]
Registers:
[0, 10, 4, 0, 0, 0, 0, 0, 0, 0]
Memory:
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

Cycle:
8
Pipeline 1:
[-1, -1, 2, -1, -1]
Pipeline 2:
[-1, 3, -1, -1, -1]
Registers:
[0, 10, 4, 0, 0, 0, 0, 0, 0, 0]
Memory:
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

Cycle:
9
Pipeline 1:
[-1, -1, -1, 2, -1]
Pipeline 2:
[-1, 3, -1, -1, -1]
Registers:
[0, 10, 4, 0, 0, 0, 0, 0, 0, 0]
Memory:
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

Cycle:
10
Pipeline 1:
[-1, -1, -1, -1, 2]
Pipeline 2:
[-1, 3, -1, -1, -1]
Registers:
[0, 10, 4, 0, 0, 0, 0, 0, 0, 0]
Memory:
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

Cycle:
11
Pipeline 1:
[-1, -1, -1, -1, -1]
Pipeline 2:
[-1, -1, 3, -1, -1]
Registers:
[0, 40, 4, 0, 0, 0, 0, 0, 0, 0]
Memory:
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

Cycle:
12
Pipeline 1:
[-1, -1, -1, -1, -1]
Pipeline 2:
[-1, -1, -1, 3, -1]
Registers:
[0, 40, 4, 0, 0, 0, 0, 0, 0, 0]
Memory:
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

Cycle:
13
Pipeline 1:
[-1, -1, -1, -1, -1]
Pipeline 2:
[-1, -1, -1, -1, 3]
Registers:
[0, 40, 4, 0, 0, 0, 0, 0, 0, 0]
Memory:
[0, 0, 0, 0, 0, 40, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

Cycle:
14
Pipeline 1:
[-1, -1, -1, -1, -1]
Pipeline 2:
[-1, -1, -1, -1, -1]
Registers:
[0, 40, 4, 0, 0, 0, 0, 0, 0, 0]
Memory:
[0, 0, 0, 0, 0, 40, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

```