class State:
    def __init__(self, pos=None):
        if pos is None:
            self.pos = {}
        else:
            self.pos = pos.copy()  
    
    def is_same(self, other):
        return self.pos == other.pos
    
    def __str__(self):
        return str(self.pos)


class BlocksWorldSteepest:   
    def __init__(self, blocks):
        self.blocks = blocks
        self.current = State()  
        self.goal = State()     
    
    def set_initial(self, init):
        for block in self.blocks:
            self.current.pos[block] = init[block]
    
    def set_goal(self, goal):
        for block in self.blocks:
            self.goal.pos[block] = goal[block]
    
    def heuristic(self, state):
        score = 0
        for block in self.blocks:
            if state.pos[block] == self.goal.pos[block]:
                score += 1 
        return score
    
    def is_clear(self, block, state):
        for b in self.blocks:
            if state.pos[b] == block:  
                return False
        return True  
    
    def get_successors(self, state):
        successors = []
        
        for block in self.blocks:
            if not self.is_clear(block, state):
                continue  
            
            new_state = State(state.pos) 
            new_state.pos[block] = "table"
            if not new_state.is_same(state):  
                successors.append(new_state)

            for target in self.blocks:
                if block == target:  
                    continue
                if not self.is_clear(target, state):  
                    continue
                
                new_state = State(state.pos)
                new_state.pos[block] = target
                if not new_state.is_same(state):
                    successors.append(new_state)
        
        return successors
    
    def solve(self):
        print("=" * 60)
        print("STEEPEST ASCENT HILL CLIMBING")
        print("=" * 60)
        print(f"Initial: {self.current}")
        print(f"Goal: {self.goal}")
        print(f"Initial h: {self.heuristic(self.current)}\n")

        for i in range(1000):
            if self.current.is_same(self.goal):
                print(f"\n{'='*60}")
                print(f"SUCCESS! Goal reached in {i} iterations!")
                print(f"{'='*60}")
                print(f"Final: {self.current}")
                return True
            
            successors = self.get_successors(self.current)
            print(f"\nIteration {i}:")
            print(f"  Current state: {self.current}")
            print(f"  Current heuristic: {self.heuristic(self.current)}")
            print(f"  Generated {len(successors)} successors")
            
            best = None
            best_score = self.heuristic(self.current)
            
            successor_scores = []
            for s in successors:
                score = self.heuristic(s)
                successor_scores.append((score, s))
                if score > best_score: 
                    best_score = score
                    best = s
            
            print(f"  Successor evaluations:")
            for score, s in sorted(successor_scores, key=lambda x: x[0], reverse=True):
                marker = " <- BEST" if s == best else ""
                print(f"    h={score}: {s}{marker}")

            if best is None:
                print(f"\n{'='*60}")
                print(f"STUCK at local maximum at iteration {i}")
                print(f"{'='*60}")
                print(f"Current state: {self.current}")
                print(f"Current heuristic: {self.heuristic(self.current)}")
                return False
            
            self.current = best
            print(f"  -> Moving to best successor with h={best_score}")
        
        print("\nMax iterations reached")
        return False


if __name__ == "__main__":
    blocks = ["A", "B", "C"]
    bw = BlocksWorldSteepest(blocks)

    initial = {
        "A": "table",
        "B": "A",
        "C": "table"
    }
    bw.set_initial(initial)

    goal = {
        "C": "table",
        "B": "C",
        "A": "B"
    }
    bw.set_goal(goal)
    
    bw.solve()
