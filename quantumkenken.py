from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, Aer, transpile

# Helper functions for multiplier
def ripple_carry_adder(qc, a, b, cin, cout, sum_bits):
    t0 = QuantumRegister(1, f't0_{_}_{idx}')
    t1 = QuantumRegister(1, f't1_{_}_{idx}')
    t2 = QuantumRegister(1, f't2_{_}_{idx}')
    qc.add_register(t0, t1, t2)

    qc.cx(a[0], sum_bits[0])
    qc.cx(b[0], sum_bits[0])
    qc.cx(cin, sum_bits[0])

    qc.ccx(a[0], b[0], t0[0])  
    qc.cx(a[0], t1[0])
    qc.cx(b[0], t1[0])         
    qc.ccx(cin, t1[0], t2[0])  
    qc.cx(t0[0], cout)
    qc.cx(t2[0], cout)

    qc.cx(a[1], sum_bits[1])
    qc.cx(b[1], sum_bits[1])
    qc.cx(cout, sum_bits[1])

    return qc


def shift_and_add_multiplier(qc, a, b, product):
    t0 = QuantumRegister(1, f't0_{_}_{idx}')
    t1 = QuantumRegister(1, f't1_{_}_{idx}')
    qc.add_register(t1, t2)

    qc.ccx(a[0], b[0], product[0])

    qc.ccx(a[0], b[1], t1[0])
    qc.ccx(a[1], b[0], t2[0])
    qc.cx(t1[0], product[1])
    qc.cx(t2[0], product[1])

    qc.ccx(a[1], b[1], product[2])

    qc.reset(product[3])

    return qc

boxes = [
    (3, '+', [0, 1]),   # sum-to-3 in top row
    (1,  '', [3]),      # cell 3 == 1
    (2,  '', [2]),      # cell 2 == 2
]

# answer
# 1 2
# 2 1
# 0110

q = QuantumRegister(4, 'q')
a = QuantumRegister(12, 'a')  
c = ClassicalRegister(4, 'c')
qc = QuantumCircuit(q, a, c)

qc.h(q)
num_iters = 1    

for _ in range(num_iters):
    qc.cx(q[0], a[0]); qc.cx(q[1], a[0])
    qc.cx(q[2], a[1]); qc.cx(q[3], a[1])
    qc.cx(q[0], a[2]); qc.cx(q[2], a[2])
    qc.cx(q[1], a[3]); qc.cx(q[3], a[3])

    qc.ccx(a[0], a[1], a[4])
    qc.ccx(a[2], a[3], a[5])
    qc.ccx(a[4], a[5], a[7])


    for idx, (target, op, cells) in enumerate(boxes):
        anc = a[8 + idx]
        if op == '+' and len(cells) == 2:
            a0 = QuantumRegister(2, f'a0_{_}_{idx}')
            b0 = QuantumRegister(2, f'b0_{_}_{idx}')
            s0 = QuantumRegister(2, f's0_{_}_{idx}')
            carry = QuantumRegister(1, f'c_{_}_{idx}')
            qc.add_register(a0, b0, s0, carry)

            # a0 = QuantumRegister(2, f'a0{idx}')
            # b0 = QuantumRegister(2, f'b0{idx}')
            # s0 = QuantumRegister(2, f's0{idx}')
            # carry = QuantumRegister(1, f'c{idx}')
            # qc.add_register(a0, b0, s0, carry)
            for i in range(2):
                qc.cx(q[cells[0]], a0[i])
                qc.cx(q[cells[1]], b0[i])
            cin = QuantumRegister(1, f'cin_{_}_{idx}')
            qc.add_register(cin)
            ripple_carry_adder(qc, a0, b0, cin[0], carry[0], s0)

            qc.x(s0[0]); qc.x(s0[1])
            if target & 1: qc.x(s0[0])
            if target & 2: qc.x(s0[1])
            qc.ccx(s0[0], s0[1], anc)

        elif op == '*' and len(cells) == 2:
            a0 = QuantumRegister(2, f'a0_{_}_{idx}')
            b0 = QuantumRegister(2, f'b0_{_}_{idx}')
            p0 = QuantumRegister(2, f'p0_{_}_{idx}')
            # a0 = QuantumRegister(2, f'ma{idx}')
            # b0 = QuantumRegister(2, f'mb{idx}')
            # p0 = QuantumRegister(4, f'p0{idx}')
            qc.add_register(a0, b0, p0)
            for i in range(2):
                qc.cx(q[cells[0]], a0[i])
                qc.cx(q[cells[1]], b0[i])
            shift_and_add_multiplier(qc, a0, b0, p0)
            for i in range(4):
                if target & (1 << i) == 0:
                    qc.x(p0[i])
            qc.mcx([p0[0], p0[1], p0[2], p0[3]], anc)

        elif op in ['-', '/'] and len(cells) == 2:
            qc.cx(q[cells[0]], a[11])
            qc.cx(q[cells[1]], a[11])
            qc.cx(a[11], anc)
            qc.cx(q[cells[1]], a[11])
            qc.cx(q[cells[0]], a[11])

        elif op == '' and len(cells) == 1:
            if target == 2:
                qc.cx(q[cells[0]], anc)

    qc.ccx(a[8], a[9], a[10])
    qc.ccx(a[10], a[7], a[6])
    qc.z(a[6])
    qc.ccx(a[10], a[7], a[6])
    qc.ccx(a[8], a[9], a[10])

    for idx, (target, op, cells) in reversed(list(enumerate(boxes))):
        anc = a[8 + idx]
        if op == '' and target == 2:
            qc.cx(q[cells[0]], anc)
        elif op in ['-', '/']:
            qc.cx(q[cells[1]], a[11])
            qc.cx(q[cells[0]], a[11])
            qc.cx(a[11], anc)
            qc.cx(q[cells[0]], a[11])
            qc.cx(q[cells[1]], a[11])

    qc.ccx(a[4], a[5], a[6])
    qc.cx(a[6], a[5])
    qc.ccx(a[0], a[1], a[4]); qc.ccx(a[2], a[3], a[5])
    qc.cx(q[3], a[3]); qc.cx(q[1], a[3])
    qc.cx(q[2], a[2]); qc.cx(q[0], a[2])
    qc.cx(q[1], a[0]); qc.cx(q[0], a[0])
    qc.reset(a[7])
    qc.reset(a[6])

    qc.h(q)
    qc.x(q)
    qc.h(q[3])
    qc.mcx([q[0], q[1], q[2]], q[3], ancilla_qubits=[a[6]])
    qc.h(q[3])
    qc.x(q)
    qc.h(q)

qc.measure(q, c)
backend = Aer.get_backend('aer_simulator')
tqc = transpile(qc, backend)
counts = backend.run(tqc, shots=1024).result().get_counts()
print("Results (q0q1q2q3):")
for bitstr, freq in sorted(counts.items()):
    print(f"  {bitstr[::-1]} → {freq}")

l = []
for bitstr, freq in sorted(counts.items()):
    l.append([freq, bitstr])
l.sort(reverse=True)

print(l)

print("FINAL ANSWER")
print(l[0])
