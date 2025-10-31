import random
from typing import List, Tuple, Iterable
 
Board = List[int]

Move = Tuple[int, int]

N = 8


def initial_board() -> Board:
    
    return [random.randint(0, N - 1) for _ in range(N)]


def conflicts(board: Board) -> int:
    
    count = 0
    for c1 in range(N):
        for c2 in range(c1 + 1, N):
            r1 = board[c1]
            r2 = board[c2]

            if r1 == r2:
                count += 1
            
            elif abs(r1 - r2) == (c2 - c1):
                count += 1
                
    return count


def neighbors(board: Board) -> Iterable[Move]:
    
    for c in range(N):
        current_r = board[c]
        for new_r in range(N):
            if new_r != current_r:
                yield (c, new_r)


def apply(board: Board, mv: Move) -> Board:
    
    c, r = mv
    newb = board.copy()
    newb[c] = r
    return newb

if __name__ == "__main__":
    board1 = initial_board()
    print(f"Tabuleiro Inicial: {board1}")
    
    initial_conflicts = conflicts(board1)
    print(f"Conflitos Iniciais: {initial_conflicts}")

    print("\nAlguns vizinhos (Movimentos):")
    gen_neighbors = neighbors(board1)
    for _ in range(5):
        try:
            move = next(gen_neighbors)
            print(f"  Movimento: {move}")
            
            board2 = apply(board1, move)
            print(f"    Novo Tabuleiro: {board2}")
            print(f"    Conflitos no Novo: {conflicts(board2)}")
            
        except StopIteration:
            break
            
    test_board = [0, 1, 2, 3, 4, 5, 6, 7]
    print(f"\nConflitos na diagonal {test_board}: {conflicts(test_board)}") 

    solved_board = [4, 6, 0, 3, 1, 7, 5, 2]
    print(f"Conflitos na solução {solved_board}: {conflicts(solved_board)}") 