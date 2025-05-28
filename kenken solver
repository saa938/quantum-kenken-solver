from qiskit import QuantumCircuit, transpile
from qiskit.providers.aer import QasmSimulator
from qiskit.circuit import QuantumRegister, ClassicalRegister
import itertools

def apply_n_cell_constraint(qc, qreg, flag, qubits, target, op):
    """
    Build phase flips for an n-cell KenKen cage on given qubits.
    qc: QuantumCircuit
    qreg: list of data qubits
    flag: single-qubit array [flag]
    qubits: list of indices into qreg for this cage
    target: integer target of the cage
    op: one of '', '+', '-', '*', '/'
    """
    n = len(qubits)
    for assignment in itertools.product([1,2], repeat=n):
        ok = False
        if op == '':
            ok = (assignment[0] == target)
        elif op == '+':
            ok = (sum(assignment) == target)
        elif op == '-':
            ok = (n==2 and abs(assignment[0] - assignment[1]) == target)
        elif op == '*':
            prod = 1
            for v in assignment: prod *= v
            ok = (prod == target)
        elif op == '/':
            if n==2:
                a,b = assignment
                ok = (max(a,b) / min(a,b) == target)
        if not ok:
            continue

        for idx, val in enumerate(assignment):
            if val == 1:
                qc.x(qreg[qubits[idx]])

        qc.mcx([qreg[i] for i in qubits], flag[0])
        qc.z(flag[0])
        qc.mcx([qreg[i] for i in qubits], flag[0])

        for idx, val in enumerate(assignment):
            if val == 1:
                qc.x(qreg[qubits[idx]])

def kenken_oracle(qc, qreg, flag, boxes):
    for key, op, cells in boxes:
        qubits = [i*2 + j for (i,j) in cells]
        apply_n_cell_constraint(qc, qreg, flag, qubits, key, op)

def solve_kenken_2x2_grover(boxes, shots=1024, grover_iters=1):
    qreg = QuantumRegister(4, 'q')
    flag = QuantumRegister(1, 'f')
    creg = ClassicalRegister(4, 'c')
    qc = QuantumCircuit(qreg, flag, creg)

    qc.h(qreg)
    qc.h(flag); qc.z(flag); qc.h(flag)

    kenken_oracle(qc, qreg, flag, boxes)

    for _ in range(grover_iters):
        qc.h(qreg); qc.x(qreg)
        qc.h(qreg[-1]); qc.mcx(qreg[:-1], qreg[-1]); qc.h(qreg[-1])
        qc.x(qreg); qc.h(qreg)

    qc.measure(qreg, creg)
    sim = QasmSimulator()
    result = sim.run(transpile(qc, sim), shots=shots).result()
    counts = result.get_counts()

    solutions = set()
    for bitstr in counts:
        grid = [[0]*2 for _ in range(2)]
        for idx in range(4):
            grid[idx//2][idx%2] = int(bitstr[3-idx]) + 1
        if any(len(set(row)) != 2 for row in grid): continue
        if any(len({grid[r][c] for r in range(2)}) != 2 for c in range(2)): continue
        valid = True
        for key, op, cells in boxes:
            nums = [grid[i][j] for i,j in cells]
            if op == '' and nums[0] != key: valid = False
            if op == '+' and sum(nums) != key: valid = False
            if op == '-' and abs(nums[0]-nums[1]) != key: valid = False
            if op == '*' and nums[0]*nums[1] != key: valid = False
            if op == '/' and max(nums)/min(nums) != key: valid = False
        if valid:
            solutions.add(tuple(tuple(row) for row in grid))
    return solutions

if __name__ == '__main__':
    boxes = [
        # (3, '+', [(0,0),(0,1)]),
        # (2, '/', [(1,0),(1,1)]),
        # (1, '', [(1,1)]),          # example single-cell cage
        # (2, '', [(1,0)]),  
        (6, '+', [(0,0),(0,1),(1,0),(1,1)])
    ]
    sols = solve_kenken_2x2_grover(boxes, grover_iters=2)
    for g in sols:
        for i in g:
            print(i)
        print()
