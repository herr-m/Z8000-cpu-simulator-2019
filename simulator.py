"""
Z8000 RISC CPU simulator with 2 pipelines

Executes the program present in the file whose name is read from the user.
This simulator only executes the following instructions:
    LOAD register address
    STORE address register
    MOVE destination source
    MVC destination constant
    IADD destination source
    IMUL destination source
"""

from copy import deepcopy


def printState(c, p1, p2, Reg, Mem):
    print("Cycle:")
    print(c)
    print("Pipeline 1:")
    print(p1)
    print("Pipeline 2:")
    print(p2)
    print("Registers:")
    print(Reg)
    print("Memory:")
    print(Mem)


class Z8000:
    def __init__(self):
        """
        Initializes all attributes of the CPU.
        :return: None
        """
        self.mem = [0 for _ in range(16)]
        self.reg = [0 for _ in range(10)]
        self.p1 = [-1 for _ in range(5)]
        self.p2 = [-1 for _ in range(5)]
        self.pc = 0
        self.mdr = 0
        self.alu_output = 0
        self.raw_prog = []
        self.prog = []
        self.timers = []
        self.state = []
        self.cycle = 1

    def load(self, file):
        """
        Loads the contents of the file 'file' into self.raw_prog
        :param: (str) file: path to the file containing the program
        :return: None
        """
        with open(file) as f:
            for instr in f:
                self.raw_prog.append(instr.strip())

        self.start_timers()

    def start_timers(self):
        """
        Initializes the timers and states for each stage of each instruction.
        The timers will determine how long each instruction must spend in a given stage.
        The states determine if the stage has already been executed.
        :return: None
        """
        for instr in self.raw_prog:
            instr_type = instr.strip().split(" ")[0]
            if instr_type == "LOAD":
                self.timers.append([0, 0, 0, 1, 0])
            elif instr_type == "STORE" or instr_type == "MOVE" or instr_type == "MVC" or instr_type == "IADD":
                self.timers.append([0, 0, 0, 0, 0])
            elif instr_type == "IMUL":
                self.timers.append([0, 0, 2, 0, 0])
            self.state.append([False for _ in range(5)])

    def avancer_pipelines(self):
        """
        Advances each instruction in its pipeline (if possible).
        Uses deepcopy to copy the pipelines at the beginning of execution to avoid advancing a pipeline by mistake.
        :return: None
        """
        p1_temp = deepcopy(self.p1)
        p2_temp = deepcopy(self.p2)
        #  Pipeline 1
        if self.p1[4] != -1:
            if self.timers[self.p1[4]][4] == 0:
                self.p1[4] = -1
            else:
                self.timers[self.p1[4]][4] -= 1

        for i in range(3, -1, -1):
            if self.p1[i] != -1:
                if self.timers[self.p1[i]][i] == 0:
                    if self.p1[i + 1] == -1:
                        ok = True
                        if i == 1:
                            # tests if the instruction self.p1[i] can go from ID to EX
                            params = self.raw_prog[self.p1[i]].split()[1:]
                            for j in range(4):
                                if j != 1 and ok and self.p1[j] != -1 and \
                                        (params[0] in self.raw_prog[self.p1[j]] or params[1] in self.raw_prog[self.p1[j]]) and \
                                        (self.p1[i] > self.p1[j]):
                                    ok = False
                                if ok and p2_temp[j] != -1 and \
                                        (params[0] in self.raw_prog[self.p2[j]] or params[1] in self.raw_prog[p2_temp[j]]) and \
                                        (self.p1[i] > p2_temp[j]):
                                    ok = False

                        if ok:
                            self.p1[i + 1] = self.p1[i]
                            self.p1[i] = -1
                else:
                    self.timers[self.p1[i]][i] -= 1

        #  Pipeline 2
        if self.p2[4] != -1:
            if self.timers[self.p2[4]][4] == 0:
                self.p2[4] = -1
            else:
                self.timers[self.p2[4]][4] -= 1

        for i in range(3, -1, -1):
            if self.p2[i] != -1:
                if self.timers[self.p2[i]][i] == 0:
                    if self.p2[i + 1] == -1:
                        ok = True
                        if i == 1:
                            # tests if the instruction self.p2[i] can go from ID to EX
                            params = self.raw_prog[self.p2[i]].split()[1:]
                            for j in range(4):
                                if ok and p1_temp[j] != -1 and \
                                        (self.p2[i] > p1_temp[j]) and \
                                        (params[0] in self.raw_prog[p1_temp[j]] or params[1] in self.raw_prog[p1_temp[j]]):
                                    ok = False
                                if j != 1 and ok and self.p2[j] != -1 and \
                                        (params[0] in self.raw_prog[self.p2[j]] or params[1] in self.raw_prog[self.p2[j]]) and \
                                        (self.p2[i] > self.p2[j]):
                                    ok = False

                        if ok:
                            self.p2[i + 1] = self.p2[i]
                            self.p2[i] = -1
                else:
                    self.timers[self.p2[i]][i] -= 1

        self.cycle += 1

    def executer_pipelines(self):
        """
        Executes each stage of each pipeline if it has not already been executed and if its timer is at 0.
        :return: None
        """
        for i in range(5):
            for p in (self.p1, self.p2):
                if p[i] != -1 and self.timers[p[i]][i] == 0 and not self.state[p[i]][i]:
                    if i == 0:
                        self.fetch(p[i])
                    elif i == 1:
                        self.decode(p[i])
                    elif i == 2:
                        self.execute(p[i])
                    elif i == 3:
                        self.mem_access(p[i])
                    else:
                        self.writeback(p[i])
                    self.state[p[i]][i] = True

    def fetch(self, instr):
        """
        Places the instruction 'instr' in self.prog
        :param instr: (int) number of the instruction in self.prog
        :return: None
        """
        self.prog.append(self.raw_prog[instr])

    def decode(self, instr):
        """
        Replaces the instruction 'instr' in self.prog by a tuple with numerical values.
        ex. "MVC R0 10" -> (3, 0, 10)
        :param instr: (int) number of the instruction in self.prog
        :return: None
        """
        self.prog[instr] = self.prog[instr].strip().split(" ")
        if self.prog[instr][0] == "LOAD":
            self.prog[instr] = (0, int(self.prog[instr][1][1]), int(self.prog[instr][2]))
        elif self.prog[instr][0] == "STORE":
            self.prog[instr] = (1, int(self.prog[instr][1]), int(self.prog[instr][2][1]))
        elif self.prog[instr][0] == "MOVE":
            self.prog[instr] = (2, int(self.prog[instr][1][1]), int(self.prog[instr][2][1]))
        elif self.prog[instr][0] == "MVC":
            self.prog[instr] = (3, int(self.prog[instr][1][1]), int(self.prog[instr][2]))
        elif self.prog[instr][0] == "IADD":
            self.prog[instr] = (4, int(self.prog[instr][1][1]), int(self.prog[instr][2][1]))
        elif self.prog[instr][0] == "IMUL":
            self.prog[instr] = (5, int(self.prog[instr][1][1]), int(self.prog[instr][2][1]))
        else:
            raise Exception("Invalid instruction!")

    def execute(self, instr):
        """
        Executes the instruction 'instr':
            For the 'STORE' instruction, places the value to write in self.mdr.
            For the 'IADD' or 'IMUL' instruction, places the result of the operation in self.alu_ouput
        :param instr: (int) number of the instruction in self.prog
        :return: None
        """
        if self.prog[instr][0] == 1:  # STORE
            self.mdr = self.reg[self.prog[instr][2]]
        elif self.prog[instr][0] == 4:  # IADD
            self.alu_output = self.reg[self.prog[instr][1]] + self.reg[self.prog[instr][2]]
        elif self.prog[instr][0] == 5:  # IMUL
            self.alu_output = self.reg[self.prog[instr][1]] * self.reg[self.prog[instr][2]]

    def mem_access(self, instr):
        """
        Reads a value from memory and places it in self.mdr, or writes the value of self.mdr in memory.
        :param instr: (int) number of the instruction in self.prog
        :return: None
        """
        if self.prog[instr][0] == 0:  # LOAD
            self.mdr = self.mem[self.prog[instr][2]]
        elif self.prog[instr][0] == 1:  # STORE
            self.mem[self.prog[instr][1]] = self.mdr

    def writeback(self, instr):
        """
        Writes a value in a working register, this value can, depending of the instruction, be in
        another register, in self.mdr, in self.alu_ouptut or can be a constant
        :param instr: (int) number of the instruction in self.prog
        :return: None
        """
        if self.prog[instr][0] == 0:  # LOAD
            self.reg[self.prog[instr][1]] = self.mdr
        elif self.prog[instr][0] == 2:  # MOVE
            self.reg[self.prog[instr][1]] = self.reg[self.prog[instr][2]]
        elif self.prog[instr][0] == 3:  # MVC
            self.reg[self.prog[instr][1]] = self.prog[instr][2]
        elif self.prog[instr][0] == 4 or self.prog[instr][0] == 5:  # IADD ou IMUL
            self.reg[self.prog[instr][1]] = self.alu_output

    def run(self):
        """
        Places the instructions in the pipelines, executes the instructions and advances the pipelines
        until all instructions have passed the writeback stage
        :return: None
        """
        # places the first instruction(s) in the fetch stage of the pipelines
        if self.pc < len(self.raw_prog) and self.p1[0] == -1:
            self.p1[0] = self.pc
            self.pc += 1
        if self.pc < len(self.raw_prog) and self.p2[0] == -1:
            self.p2[0] = self.pc
            self.pc += 1

        while set(self.p1) != {-1} or set(self.p2) != {-1}:
            # places the next instruction(s) in the fetch stage
            if self.pc < len(self.raw_prog) and self.p1[0] == -1:
                self.p1[0] = self.pc
                self.pc += 1
            if self.pc < len(self.raw_prog) and self.p2[0] == -1:
                self.p2[0] = self.pc
                self.pc += 1

            printState(self.cycle, self.p1, self.p2, self.reg, self.mem)
            self.executer_pipelines()
            self.avancer_pipelines()


if __name__ == "__main__":
    file = input()
    processor = Z8000()
    processor.load(file)
    processor.run()

    printState(processor.cycle, processor.p1, processor.p2, processor.reg, processor.mem)
