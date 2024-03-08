# c: cycle number
# p1 et p2: lists of length 5, representing each of the 5 operations of an instruction.
# Reg: list of length 10, representing the contents of the registers
# Mem: list of length 16, representing the contents of the memory

def printState(c, p1, p2, Reg, Mem):
    print("Cycle:")
    print(c)
    print("Pipeline 1:")
    print(p1)
    print("Pipeline 2:")
    print(p2)
    print("Registres:")
    print(Reg)
    print("Memoire:")
    print(Mem)

def main():
    # Example
    M = [0 for x in range(16)] # Memory
    M[3] = 10
    
    R = [0 for x in range(10)] # Registers
    R[2] = 7
    
    # Pipelines
    p1 = [4,  2,  0, -1, -1]
    p2 = [3,  1, -1, -1, -1]
    
    printState(3, p1, p2, R, M)


if __name__ == '__main__':
    main()
