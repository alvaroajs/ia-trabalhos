

from typing import List, Tuple
 
Grid = List[List[str]]
Pos = Tuple[int, int]

class Maze:
     
    def __init__(self, filename: str):
       
        try:
            with open(filename, 'r') as f:
                self.grid = [list(line.strip()) for line in f.readlines()]
        except FileNotFoundError:
            raise FileNotFoundError(f"Erro: O arquivo '{filename}' não foi encontrado.")
        
        self.H = len(self.grid) 
        self.W = len(self.grid[0]) if self.H > 0 else 0 
        
        self.start = self._find('S')
        self.goal = self._find('G')

    def _find(self, char: str) -> Pos:
        for r in range(self.H):
            for c in range(self.W):
                if self.grid[r][c] == char:
                    return (r, c)
        raise ValueError(f"Caractere '{char}' não encontrado no grid")

    def in_bounds(self, p: Pos) -> bool:
        r, c = p
        return 0 <= r < self.H and 0 <= c < self.W

    def passable(self, p: Pos) -> bool:
        r, c = p
        return self.grid[r][c] != '#'

    def actions(self, p: Pos) -> List[str]:
        acts = []
        r, c = p
        candidates = {
            'N': (r - 1, c),
            'S': (r + 1, c),
            'O': (r, c - 1),
            'L': (r, c + 1)
        }
        
        for action, (nr, nc) in candidates.items():
            q = (nr, nc)
            if self.in_bounds(q) and self.passable(q):
                acts.append(action)
        return acts

    def result(self, p: Pos, a: str) -> Pos:
        r, c = p
        delta = {'N': (-1, 0), 'S': (1, 0), 'O': (0, -1), 'L': (0, 1)}
        dr, dc = delta[a]
        q = (r + dr, c + dc)
        
        if not (self.in_bounds(q) and self.passable(q)):
            raise ValueError(f"Ação '{a}' inválida na posição {p}")
        return q

    def step_cost(self, p_from: Pos, action: str, p_to: Pos) -> float:
        return 1.0

    def goal_test(self, p: Pos) -> bool:
        return p == self.goal

if __name__ == '__main__':
    maze_filepath = '../data/labirinto.txt'
    
    print(f"Tentando carregar o labirinto de: {maze_filepath}")
    
    try:
        mz = Maze(maze_filepath)
        
        print("Labirinto carregado com sucesso!")
        print(f"Dimensões: {mz.H}x{mz.W}")
        print(f"Posição Inicial (S): {mz.start}")
        print(f"Posição Objetivo (G): {mz.goal}")
        
        start_actions = mz.actions(mz.start)
        print(f"Ações válidas em S {mz.start}: {start_actions}")

        if start_actions:
            first_action = start_actions[0]
            next_pos = mz.result(mz.start, first_action)
            print(f"Após mover '{first_action}' de {mz.start}, a nova posição é {next_pos}")

    except (FileNotFoundError, ValueError) as e:
        print(e)