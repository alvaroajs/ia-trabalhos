from typing import Tuple
 
Pos = Tuple[int, int]

def h_manhattan(a: Pos, b: Pos) -> float:
    
    (r1, c1) = a
    (r2, c2) = b
    return float(abs(r1 - r2) + abs(c1 - c2))
 
def h_euclidean(a: Pos, b: Pos) -> float:
    
    (r1, c1) = a
    (r2, c2) = b
    return ((r1 - r2) ** 2 + (c1 - c2) ** 2) ** 0.5