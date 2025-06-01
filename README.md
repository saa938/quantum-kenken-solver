# **quantum-kenken-solver**

**We are running this on Qiskit v0.43**

Go to Anaconda Powershell and run these commands to install necessary libraries
```
conda create -n qiskit043 python=3.9
conda activate qiskit043
pip install qiskit==0.43
```

---

## **Ken Ken**

KenKen is a logic-based numerical puzzle that combines elements of **Sudoku** and **arithmetic**. The puzzle consists of a grid. The grid is divided into _"cages,"_ each with a **target number** and a **mathematical operation** (addition, subtraction, multiplication, division, and sometimes single cell cages with no operation). The goal is to fill the grid with numbers while ensuring that:
- Each **row and column** contains unique numbers.
- The numbers within each cage satisfy the given **mathematical operation** to reach the target number.

---

## **Quantum Computer**

A quantum computer is a super cool kind of computer that uses **qubits**. Unlike regular bits that are either `0` or `1`, qubits can be `0` **and** `1` at the same time (called **superposition**). This lets us try out many possibilities all at once — a bit like solving every possible answer in parallel.

---

## **Grover's Algorithm**

Grover's algorithm is a **quantum search algorithm** that finds a specific item in an unsorted database faster than classical methods. It achieves this by **amplifying the probability** of the correct answer through repeated quantum operations, reducing the number of searches needed from `N` to `√N`.

---

## **Time Complexity**

A classical solution could be trying out all possible combinations and checking if they work, resulting in **O(N!^(N)*(N²))** time complexity. However, since we use Grover's algorithm there is a **quadratic speedup**, and our new time complexity is **O(√(N!^(N)*(N²)))**.

---

## **Encoding the Problem**

First, we make each KenKen square into a qubit. Since the grid is 2x2, we have **4 qubits**, and we can say that:
- `0` means there is a **1** in that square.
- `1` means that there is a **2** in that square.

(Since there can only be 2 possible numbers in a 2x2 KenKen.)

We apply a **Hadamard (H)** gate to all the qubits and prepare the **ancilla flag qubit**.

---

## **Oracle Construction**

We have to check:
- If the **rows and columns** are different
- If the **boxes** (cages) are satisfied

There are two parts to the oracle: the **row/column** part and the **box** part.

### **Row/Column Constraint**

We check if:
```
((q0 xor q1) & (q2 xor q3)) & ((q0 xor q2) & (q1 xor q3))
```

#### **XOR Logic**
We can create an ancilla qubit at 0:
- `CNOT(q1, ancilla)`
- `CNOT(q2, ancilla)`

If ancilla is 0 → they’re the same; if 1 → they’re different.

#### **AND Logic**
Create another ancilla qubit at 0:
- Use a **Toffoli (CCX)** gate:
  - Controls: a1 and a2
  - Target: a3
  - If a3 is 1 → both a1 and a2 were 1

#### **Implementation Idea**

Ancilla bits: `a1` to `a7`, all initialized to 0.

```
CNOT(q0, a1)
CNOT(q1, a1)

CNOT(q2, a2)
CNOT(q3, a2)

CNOT(q0, a3)
CNOT(q2, a3)

CNOT(q1, a4)
CNOT(q3, a4)

CCX(a1, a2, a5)
CCX(a3, a4, a6)
CCX(a5, a6, a7)
```

If `a7` is 1, then the **rows and columns are all different**, otherwise they’re not. Our **target solution** will have it as 1.

---

## **Box Constraint**

- **Addition**: Use **ripple carry adder**, then XOR to compare to target.
- **Subtraction**: Convert to 2’s complement, then add and XOR to compare.
- **Multiplication**: Use **shift-and-add multiplier**, then XOR to compare.
- **Division**: If `b / s = t`, then `ts = b` → use multiplication.

### **2x2 Shortcut**

Since all subtraction and division constraints in a 2x2 grid have 2 cells and must be 1:
- Just **check if they’re different**

This saves memory.

---

## **Box Input Format**

```python
boxes = [
    (3, '+', [0, 1]),
    (1, '', [3]),          
    (2, '', [2]),  
]
```

- Format: `(target, operation, [cells])`
- Cells: `0 = top-left`, `1 = top-right`, `2 = bottom-left`, `3 = bottom-right`

---

## **Final Combination**

Use **AND** gates to combine:
- All box constraints
- `a7` from rows/columns

Let the final ancilla qubit comparing all constraints be `a_final`, then:

```python
qc.z(a_final)
```

---

## **Grover Amplification**

To amplify the marked states:
1. Apply **Hadamard** to all qubits
2. Apply **X** gates
3. Apply **MCX** (multi-controlled X) gate
4. Undo the X and H gates

This amplifies the probability of correct states.

---

## **Measurement and Output**

- Measure the **data qubits** (not ancilla).
- Interpret the bitstrings and print the solution.

---

## **Limitations**

We don't have enough memory to run the Grover loop multiple times.  
If we could, our code would be **more accurate**. Right now, because we have one iteration of Grover's algorithm, and since we have 16 states, the probability of getting the correct state is 47%. To make it get 95-99 percent accuracy, we would have to have at least 3 Grover iterations for a 2x2 Ken Ken. A possible solution is to create more short cuts for addition and multiplication as well abusing the fact that the Ken Ken is 2x2.
