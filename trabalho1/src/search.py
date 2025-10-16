import heapq
import time
import tracemalloc  
from typing import List, Tuple, Dict, Optional
 
from maze import Maze, Pos
from heuristics import h_manhattan

def a_star_search(maze: Maze) -> Tuple[Optional[List[Pos]], Optional[float]]:
    start_node = maze.start
    goal_node = maze.goal
    
    frontier = [(h_manhattan(start_node, goal_node), start_node)]
    
    came_from: Dict[Pos, Pos] = {}
    
    cost_so_far: Dict[Pos, float] = {start_node: 0.0}

    while frontier:
        _, current_node = heapq.heappop(frontier)

        if maze.goal_test(current_node):
            path = []
            temp = current_node
            while temp in came_from:
                path.append(temp)
                temp = came_from[temp]
            path.append(start_node)
            path.reverse() 
            return path, cost_so_far[current_node]
  
        for action in maze.actions(current_node): 
            neighbor = maze.result(current_node, action)
             
            new_cost = cost_so_far[current_node] + maze.step_cost(current_node, action, neighbor)
             
            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                 
                priority = new_cost + h_manhattan(neighbor, goal_node)
                 
                heapq.heappush(frontier, (priority, neighbor))
                 
                came_from[neighbor] = current_node
  
    return None, None

def greedy_best_first_search(maze: Maze) -> Tuple[Optional[List[Pos]], Optional[float]]:
    start_node = maze.start
    goal_node = maze.goal
    
    frontier = [(h_manhattan(start_node, goal_node), start_node)]
    
    came_from: Dict[Pos, Pos] = {start_node: None}
    
    explored = {start_node}

    cost_so_far: Dict[Pos, float] = {start_node: 0.0}

    while frontier:
        _, current_node = heapq.heappop(frontier)

        if maze.goal_test(current_node):
            path = []
            temp = current_node
            while temp is not None:
                path.append(temp)
                temp = came_from[temp]
            path.reverse()
            return path, cost_so_far[current_node]
  
        for action in maze.actions(current_node): 
            neighbor = maze.result(current_node, action)
            
            if neighbor not in explored:
                explored.add(neighbor)
                
                cost_so_far[neighbor] = cost_so_far[current_node] + maze.step_cost(current_node, action, neighbor)
                came_from[neighbor] = current_node
                
                priority = h_manhattan(neighbor, goal_node)
                heapq.heappush(frontier, (priority, neighbor))
  
    return None, None
 
if __name__ == '__main__':
    try:    
        maze_instance = Maze('../data/labirinto.txt')
        
        print("Labirinto carregado.")
        print(f"Início: {maze_instance.start}, Objetivo: {maze_instance.goal}\n")
 
        print("Executando A*...")
        tracemalloc.start()    
        start_time_a_star = time.perf_counter()
        
        a_star_path, a_star_cost = a_star_search(maze_instance)
        
        end_time_a_star = time.perf_counter()
        _, peak_mem_a_star = tracemalloc.get_traced_memory() 
        tracemalloc.stop()   
        
        elapsed_time_a_star = end_time_a_star - start_time_a_star
        print(f"A* concluído em {elapsed_time_a_star:.6f} segundos.")
        print(f"Pico de memória (A*): {peak_mem_a_star / 1024:.2f} KB")

 
        print("\nExecutando Busca Gulosa...")
        tracemalloc.start() 
        start_time_greedy = time.perf_counter()

        greedy_path, greedy_cost = greedy_best_first_search(maze_instance)
        
        end_time_greedy = time.perf_counter()
        _, peak_mem_greedy = tracemalloc.get_traced_memory() 
        tracemalloc.stop()  

        elapsed_time_greedy = end_time_greedy - start_time_greedy
        print(f"Busca Gulosa concluída em {elapsed_time_greedy:.6f} segundos.")
        print(f"Pico de memória (Busca Gulosa): {peak_mem_greedy / 1024:.2f} KB")

        output_filepath = '../data/results.txt'

        if a_star_path or greedy_path:
            print(f"\nSalvando resultados em {output_filepath}...")

            a_star_result_content = "Nenhuma solução encontrada pelo algoritmo A*."
            if a_star_path:
                a_star_result_content = (
                    f"Algoritmo: A*\n"
                    f"Tempo de execução: {elapsed_time_a_star:.6f} segundos\n"
                    f"Pico de memória: {peak_mem_a_star / 1024:.2f} KB\n"
                    f"Custo do caminho: {a_star_cost}\n"
                    f"Nós no caminho: {len(a_star_path)}\n"
                    f"Caminho: {a_star_path}\n"
                )

            greedy_result_content = "Nenhuma solução encontrada pelo algoritmo Greedy Best-First Search."
            if greedy_path:
                greedy_result_content = (
                    f"Algoritmo: Greedy Best-First Search\n"
                    f"Tempo de execução: {elapsed_time_greedy:.6f} segundos\n"
                    f"Pico de memória: {peak_mem_greedy / 1024:.2f} KB\n"
                    f"Custo do caminho: {greedy_cost}\n"
                    f"Nós no caminho: {len(greedy_path)}\n"
                    f"Caminho: {greedy_path}\n"
                )
            
            with open(output_filepath, 'w', encoding='utf-8') as f:
                f.write(a_star_result_content)
                f.write("\n--------------------------------------------------\n\n")
                f.write(greedy_result_content)
            
            print("Resultados salvos com sucesso. ✅")

        else:
            print("\nNenhuma solução foi encontrada por ambos os algoritmos. ❌")
            with open(output_filepath, 'w', encoding='utf-8') as f:
                f.write("Nenhuma solução foi encontrada por ambos os algoritmos.\n")

    except (FileNotFoundError, ValueError) as e:
        print(f"Ocorreu um erro: {e}")