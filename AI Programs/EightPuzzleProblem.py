import heapq

class State:
    def __init__(self, board, g, h, parent=None, move=""):
        self.board = board
        self.g = g
        self.h = h
        self.f = g + h
        self.parent = parent
        self.move = move
    
    def __lt__(self, other):
        return self.f < other.f


def find_blank(board):
    for i in range(3):
        for j in range(3):
            if board[i][j] == 0:
                return i, j


def misplaced_tiles(board, goal):
    count = 0
    for i in range(3):
        for j in range(3):
            if board[i][j] != 0:  
                if board[i][j] != goal[i][j]:
                    count += 1
    return count


def get_neighbors(state, goal):
    neighbors = []
    i, j = find_blank(state.board)
    moves = [("UP", -1, 0), ("DOWN", 1, 0), ("LEFT", 0, -1), ("RIGHT", 0, 1)]
    
    for name, di, dj in moves:
        ni, nj = i + di, j + dj
        if 0 <= ni < 3 and 0 <= nj < 3:
            new_board = [row[:] for row in state.board]
            new_board[i][j], new_board[ni][nj] = new_board[ni][nj], new_board[i][j]
            h = misplaced_tiles(new_board, goal)
            neighbors.append(State(new_board, state.g + 1, h, state, name))
    
    return neighbors


def solve_puzzle(initial, goal):
    h = misplaced_tiles(initial, goal)
    start = State(initial, 0, h)
    
    open_list = [start]
    visited = set()
    
    while open_list:
        current = heapq.heappop(open_list)
        
        if current.board == goal:
            return current
        
        visited.add(str(current.board))
        
        for neighbor in get_neighbors(current, goal):
            if str(neighbor.board) not in visited:
                heapq.heappush(open_list, neighbor)
    
    return None


def print_solution(solution):
    if not solution:
        print("No solution found")
        return
    
    path = []
    current = solution
    while current:
        path.append(current)
        current = current.parent
    path.reverse()
    
    print(f"Solution in {len(path)-1} moves:\n")
    for i, state in enumerate(path):
        print(f"Step {i}: {state.move} (g={state.g}, h={state.h}, f={state.f})")
        for row in state.board:
            print(" ".join(str(x) for x in row))
        print()


if __name__ == "__main__":
    initial = [[1,2,3], [4,0,5], [7,8,6]]
    goal = [[1,2,3], [4,5,6], [7,8,0]]
    
    print("A* with MISPLACED TILES heuristic\n")
    solution = solve_puzzle(initial, goal)
    print_solution(solution)
