import itertools

def check_kenken(grid, boxes):
    n = len(grid)
    for i in range(n):
        if set(grid[i]) != set(range(1, n + 1)):
            return False

    for j in range(n):
        col = {grid[i][j] for i in range(n)}
        if col != set(range(1, n + 1)):
            return False

    for box in boxes:
        key, operation = box[0], box[1]
        if operation == '':
            (r, c), = box[2]
            if grid[r][c] != key:
                return False
            else:
                continue

        cells = box[2]     
        nums = [grid[r][c] for (r, c) in cells]

        if operation == '+':
            if sum(nums) != key:
                return False
        elif operation == '-':
            if abs(nums[0] - nums[1]) != key:
                return False
        elif operation == '*':
            prod = 1
            for v in nums:
                prod *= v
            if prod != key:
                return False
        elif operation == '/':
            a, b = max(nums), min(nums)
            if a % b != 0 or (a // b) != key:
                return False
        else:
            return False

    return True


def solve_2x2_kenken(boxes):
    n = 2
    all_perms = list(itertools.permutations(range(1, n + 1))) 

    for i in all_perms:
        for j in all_perms:
            if i[0] == j[0] or i[1] == j[1]:continue

            cand = [list(i), list(j)]
            if check_kenken(cand, boxes):return cand

    return None


boxes = [
    (2, '-', [(0, 0), (0, 1)]),   
    (2, '',  [(1, 0)]),          
    (1, '',  [(1, 1)]),          
]

solution = solve_2x2_kenken(boxes)
if solution:
    for row in solution:
        print(row)
else:
    print("No solution")
