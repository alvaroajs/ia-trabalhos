import random
import time
from typing import List, Tuple, Optional
from eight_queens import Board, initial_board, conflicts, neighbors, apply

HillClimbingResult = Tuple[Board, int, int]

def hill_climbing_padrao(max_iterations: int) -> HillClimbingResult:
    current_board = initial_board()
    current_conflicts = conflicts(current_board)
    
    for i in range(max_iterations):
        if current_conflicts == 0:
            return current_board, 0, i

        best_neighbor = None
        min_neighbor_conflicts = current_conflicts

        moves = list(neighbors(current_board))
        random.shuffle(moves)

        for mv in moves:
            neighbor = apply(current_board, mv)
            neighbor_conflicts = conflicts(neighbor)
            
            if neighbor_conflicts < min_neighbor_conflicts:
                min_neighbor_conflicts = neighbor_conflicts
                best_neighbor = neighbor
        
        if best_neighbor is None:
            return current_board, current_conflicts, i

        current_board = best_neighbor
        current_conflicts = min_neighbor_conflicts
            
    return current_board, current_conflicts, max_iterations

def hill_climbing_movimentos_laterais(max_iterations: int, max_lateral_moves: int) -> HillClimbingResult:
    current_board = initial_board()
    current_conflicts = conflicts(current_board)
    lateral_moves_count = 0
    
    for i in range(max_iterations):
        if current_conflicts == 0:
            return current_board, 0, i

        best_neighbor = None
        min_neighbor_conflicts = float('inf')

        moves = list(neighbors(current_board))
        random.shuffle(moves)

        if not moves:
            return current_board, current_conflicts, i

        best_neighbor = apply(current_board, moves[0])
        min_neighbor_conflicts = conflicts(best_neighbor)

        for mv in moves[1:]:
            neighbor = apply(current_board, mv)
            neighbor_conflicts = conflicts(neighbor)
            
            if neighbor_conflicts < min_neighbor_conflicts:
                min_neighbor_conflicts = neighbor_conflicts
                best_neighbor = neighbor
        
        if min_neighbor_conflicts > current_conflicts:
            return current_board, current_conflicts, i
        elif min_neighbor_conflicts == current_conflicts:
            lateral_moves_count += 1
            if lateral_moves_count >= max_lateral_moves:
                return current_board, current_conflicts, i
        else:
            lateral_moves_count = 0
        
        current_board = best_neighbor
        current_conflicts = min_neighbor_conflicts
            
    return current_board, current_conflicts, max_iterations

def hill_climbing_reinicios_aleatorios(max_restarts: int, max_iterations_per_restart: int) -> HillClimbingResult:
    best_board = None
    best_conflicts = float('inf')
    total_steps_all_restarts = 0
    
    for _ in range(max_restarts):
        current_board = initial_board()
        current_conflicts = conflicts(current_board)
        
        board_at_local_optimum = current_board
        conflicts_at_local_optimum = current_conflicts
        
        steps_this_restart = 0

        for i in range(max_iterations_per_restart):
            steps_this_restart = i + 1
            
            if current_conflicts == 0:
                total_steps_all_restarts += steps_this_restart
                return current_board, 0, total_steps_all_restarts

            best_neighbor = None
            min_neighbor_conflicts = current_conflicts

            moves = list(neighbors(current_board))
            random.shuffle(moves)

            for mv in moves:
                neighbor = apply(current_board, mv)
                neighbor_conflicts = conflicts(neighbor)
                
                if neighbor_conflicts < min_neighbor_conflicts:
                    min_neighbor_conflicts = neighbor_conflicts
                    best_neighbor = neighbor
            
            if best_neighbor is None:
                board_at_local_optimum = current_board
                conflicts_at_local_optimum = current_conflicts
                break

            current_board = best_neighbor
            current_conflicts = min_neighbor_conflicts
        
        else:
            board_at_local_optimum = current_board
            conflicts_at_local_optimum = current_conflicts
        
        total_steps_all_restarts += steps_this_restart
        
        if conflicts_at_local_optimum < best_conflicts:
            best_conflicts = conflicts_at_local_optimum
            best_board = board_at_local_optimum
    
    return best_board, best_conflicts, total_steps_all_restarts

def print_metrics(name: str, results: List[Tuple[bool, int, float]]):
    total_runs = len(results)
    if total_runs == 0:
        print(f"Sem resultados para {name}")
        return

    successes = [r[0] for r in results].count(True)
    success_rate = (successes / total_runs) * 100
    
    total_time = sum(r[2] for r in results)
    avg_time_per_run = total_time / total_runs
    
    successful_runs = [r for r in results if r[0]]
    failed_runs = [r for r in results if not r[0]]

    if successful_runs:
        avg_steps_to_solution = sum(r[1] for r in successful_runs) / len(successful_runs)
    else:
        avg_steps_to_solution = float('nan')
        
    if failed_runs:
        avg_steps_on_failure = sum(r[1] for r in failed_runs) / len(failed_runs)
    else:
        avg_steps_on_failure = float('nan')

    print(f"\n--- Métricas para: {name} ---")
    print(f"  Execuções Totais:   {total_runs}")
    print(f"  Taxa de Sucesso:    {success_rate:.2f}% ({successes}/{total_runs})")
    print(f"  Tempo Total:        {total_time:.4f} s")
    print(f"  Tempo Médio/Exec.:  {avg_time_per_run:.6f} s")
    print(f"  Média Passos (Sucesso): {avg_steps_to_solution:.2f}")
    print(f"  Média Passos (Falha):   {avg_steps_on_failure:.2f}")
    print("--------------------------------" + "-" * len(name))

if __name__ == '__main__':
    print("Iniciando experimentos com o Problema das 8 Rainhas...")

    N_RUNS = 200

    MAX_ITER_PADRAO = 200
    MAX_ITER_LATERAL = 200
    MAX_LATERAL_MOVES = 50

    MAX_RESTARTS = 50
    MAX_ITER_PER_RESTART = 100

    results = {
        "HC Padrão": [],
        "HC Mov. Laterais": [],
        "HC Reinícios Aleatórios": []
    }

    print(f"Executando {N_RUNS} rodadas de cada algoritmo...")

    for i in range(N_RUNS):
        start_time = time.perf_counter()
        board, cost, steps = hill_climbing_padrao(MAX_ITER_PADRAO)
        end_time = time.perf_counter()
        results["HC Padrão"].append((cost == 0, steps, end_time - start_time))

        start_time = time.perf_counter()
        board, cost, steps = hill_climbing_movimentos_laterais(MAX_ITER_LATERAL, MAX_LATERAL_MOVES)
        end_time = time.perf_counter()
        results["HC Mov. Laterais"].append((cost == 0, steps, end_time - start_time))
        
        start_time = time.perf_counter()
        board, cost, steps = hill_climbing_reinicios_aleatorios(MAX_RESTARTS, MAX_ITER_PER_RESTART)
        end_time = time.perf_counter()
        results["HC Reinícios Aleatórios"].append((cost == 0, steps, end_time - start_time))
        
        if (i + 1) % (N_RUNS / 10) == 0:
            print(f"  ... {i+1}/{N_RUNS} rodadas completas.")

    print("\nExperimentos concluídos. Compilando métricas...")

    print_metrics("HC Padrão", results["HC Padrão"])
    print_metrics("HC Mov. Laterais", results["HC Mov. Laterais"])
    print_metrics("HC Reinícios Aleatórios", results["HC Reinícios Aleatórios"])

    print("\nAnálise concluída.")
