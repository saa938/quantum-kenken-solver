# quantum-kenken-solver

Ken Ken:
KenKen is a logic-based numerical puzzle that combines elements of Sudoku and arithmetic. The puzzle consists of a grid. The grid is divided into "cages," each with a target number and a mathematical operation (addition, subtraction, multiplication, division, and sometimes single cell cages with no operation). The goal is to fill the grid with numbers while ensuring that each row and column contains unique numbers and the numbers within each cage satisfy the given mathematical operation to reach the target number.

Quantum Computer:
A quantum computer is a super cool kind of computer that uses qubits. Unlike regular bits that are either 0 or 1, qubits can be 0 and 1 at the same time (called superposition). This lets us try out many possibilities all at once—a bit like solving every possible answer in parallel.

Grover's algorithm:
Grover's algorithm is a quantum search algorithm that finds a specific item in an unsorted database faster than classical methods. It achieves this by amplifying the probability of the correct answer through repeated quantum operations, reducing the number of searches needed from N to sqrt(N).

Time Complexity: 
A classical solution could be trying out all possible combinations and checking if they work, resulting in O(N^(N^2)) time complexity. However, since we use Grover's algorithm there is a quadratic speedup and our new time complexity is O(sqrt(N^(N^2)). 

First, we make each KenKen square into a qubit. Since the grid is 2x2, we have 4 qubits, and we can say that 0 means there is a 1 in that square and a 1 means that there is a 2 in that square since there can only be 2 possible numbers in a 2x2 Ken Ken. We apply a Hadamard (H) gate to all the qubits and prepare the ancilla flag qubit.

Next, we create the Oracle. We use a multi-controlled X (MCX) gate, which is a generalization of the Toffoli gate. We use it to match valid patterns like [0,1], [1,0] and flip the ancilla qubit. The ancilla qubit is used to store whether a KenKen constraint like sum or division is satisfied. This is repeated for each cage condition. 

After this, we amplify the marked states' probabilities using Grover's algorithm. We apply a Hadamard gate on all qubits, then an X gate, then a MCX gate, and then we undo the H and X gates. This amplifies the marked states' probabilties. We then measure the quantum state to obtain a valid Ken Ken solution with a high probability, and we only measure the data qubits not the ancilla qubit. Then, we interpret the bitstrings and print out the solutions
