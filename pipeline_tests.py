prog = ["MVC R1 10", "MVC R2 4", "IMUL R1 R2", "STORE 5 R1"]
timers = []
for instr in prog:
    instr_type = instr.strip().split(" ")[0]
    if instr_type == "LOAD":
        timers.append([0, 0, 0, 1, 0])
    if instr_type == "STORE" or instr_type == "MOVE" or instr_type == "MVC" or instr_type == "IADD":
        timers.append([0, 0, 0, 0, 0])
    if instr_type == "IMUL":
        timers.append([0, 0, 2, 0, 0])

p1 = [-1, -1, -1, -1, -1]
p2 = [-1, -1, -1, -1, -1]

pc = 2

cycle = 1


def avance():
    #  Pipeline 1
    if p1[4] != -1:
        if timers[p1[4]][4] == 0:
            p1[4] = -1
        else:
            timers[p1[4]][4] -= 1

    for i in range(3, -1, -1):
        if p1[i] != -1:
            if timers[p1[i]][i] == 0:
                if p1[i + 1] == -1:
                    ok = True
                    if i == 1:
                        params = prog[p1[i]].split()[1:]
                        for j in range(4):
                            if ok and p1[j] != -1 and \
                               (params[0] in prog[p1[j]] or params[1] in prog[p1[j]]) and \
                               (p1[i] > p1[j]):
                                ok = False
                            if ok and p2[j] != -1 and \
                               (params[0] in prog[p2[j]] or params[1] in prog[p2[j]]) and \
                               (p1[i] > p2[j]):
                                ok = False
                    if ok:
                        p1[i + 1] = p1[i]
                        p1[i] = -1
            else:
                timers[p1[i]][i] -= 1

    #  Pipeline 2
    if p2[4] != -1:
        if timers[p2[4]][4] == 0:
            p2[4] = -1
        else:
            timers[p2[4]][4] -= 1

    for i in range(3, -1, -1):
        if p2[i] != -1:
            if timers[p2[i]][i] == 0:
                if p2[i + 1] == -1:
                    ok = True
                    if i == 1:
                        params = prog[p2[i]].split()[1:]
                        for j in range(4):
                            if ok and p1[j] != -1 and \
                                    (params[0] in prog[p1[j]] or params[1] in prog[p1[j]]) and \
                                    (p2[i] > p1[j]):
                                ok = False
                            if ok and p2[j] != -1 and \
                                    (params[0] in prog[p2[j]] or params[1] in prog[p2[j]]) and \
                                    (p2[i] > p2[j]):
                                ok = False

                    if ok:
                        p2[i + 1] = p2[i]
                        p2[i] = -1
            else:
                timers[p2[i]][i] -= 1


p1[0] = 0
p2[0] = 1

while set(p1) != {-1} or set(p2) != {-1}:
    if pc < len(prog):
        if p1[0] == -1:
            p1[0] = pc
            pc += 1
        if p2[0] == -1:
            p2[0] = pc
            pc += 1

    print(cycle)
    print(p1, "\n", p2)
    print()
    avance()
    cycle += 1
