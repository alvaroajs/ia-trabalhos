import heapq
import time
import tracemalloc
from collections import deque  
from typing import List, Tuple, Dict, Optional

from maze import Maze, Pos
from heuristics import h_manhattan

# --- Buscas Informadas ---

def a_star_search(maze: Maze) -> Tuple[Optional[List[Pos]], Optional[float], int]:
    """
    Realiza uma busca A*.
    Retorna: (caminho, custo, nós_expandidos)
    """
    start_node = maze.start
    goal_node = maze.goal
    
    nodes_expanded = 0
    
    frontier = [(h_manhattan(start_node, goal_node), start_node)]
    
    came_from: Dict[Pos, Pos] = {}
    
    cost_so_far: Dict[Pos, float] = {start_node: 0.0}

    while frontier:
        _, current_node = heapq.heappop(frontier)
         
        if current_node in came_from and came_from[current_node] is not None:
             if cost_so_far[current_node] > cost_so_far.get(current_node, float('inf')):
                 continue

        nodes_expanded += 1

        if maze.goal_test(current_node):
            path = []
            temp = current_node
            while temp in came_from:
                path.append(temp)
                temp = came_from[temp]
            path.append(start_node)
            path.reverse() 
            return path, cost_so_far[current_node], nodes_expanded
  
        for action in maze.actions(current_node): 
            neighbor = maze.result(current_node, action)
            new_cost = cost_so_far[current_node] + maze.step_cost(current_node, action, neighbor)
            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                priority = new_cost + h_manhattan(neighbor, goal_node)
                heapq.heappush(frontier, (priority, neighbor))
                came_from[neighbor] = current_node
  
    return None, None, nodes_expanded

def greedy_best_first_search(maze: Maze) -> Tuple[Optional[List[Pos]], Optional[float], int]:
    """
    Realiza uma Busca Gulosa.
    Retorna: (caminho, custo, nós_expandidos)
    """
    start_node = maze.start
    goal_node = maze.goal
    
    nodes_expanded = 0
    
    frontier = [(h_manhattan(start_node, goal_node), start_node)]
    
    came_from: Dict[Pos, Pos] = {start_node: None}
    
    explored = {start_node}

    cost_so_far: Dict[Pos, float] = {start_node: 0.0}

    while frontier:
        _, current_node = heapq.heappop(frontier)
        nodes_expanded += 1

        if maze.goal_test(current_node):
            path = []
            temp = current_node
            while temp is not None:
                path.append(temp)
                temp = came_from[temp]
            path.reverse()
            return path, cost_so_far[current_node], nodes_expanded
  
        for action in maze.actions(current_node): 
            neighbor = maze.result(current_node, action)
            if neighbor not in explored:
                explored.add(neighbor)
                cost_so_far[neighbor] = cost_so_far[current_node] + maze.step_cost(current_node, action, neighbor)
                came_from[neighbor] = current_node
                priority = h_manhattan(neighbor, goal_node)
                heapq.heappush(frontier, (priority, neighbor))
  
    return None, None, nodes_expanded
 

def bfs_search(maze: Maze) -> Tuple[Optional[List[Pos]], Optional[float], int]:
    """
    Realiza uma Busca em Largura (BFS).
    Retorna: (caminho, custo, nós_expandidos)
    """
    start_node = maze.start
    nodes_expanded = 0
    
    frontier = deque([start_node])  
    
    came_from: Dict[Pos, Pos] = {start_node: None}
    
    explored = {start_node}

    while frontier:
        current_node = frontier.popleft()   
        nodes_expanded += 1

        if maze.goal_test(current_node):
            path = []
            temp = current_node
            while temp is not None:
                path.append(temp)
                temp = came_from[temp]
            path.reverse()
            cost = len(path) - 1
            return path, float(cost), nodes_expanded

        for action in maze.actions(current_node):
            neighbor = maze.result(current_node, action)
            if neighbor not in explored:
                explored.add(neighbor)
                came_from[neighbor] = current_node
                frontier.append(neighbor)  

    return None, None, nodes_expanded

def dfs_search(maze: Maze) -> Tuple[Optional[List[Pos]], Optional[float], int]:
    """
    Realiza uma Busca em Profundidade (DFS).
    Retorna: (caminho, custo, nós_expandidos)
    """
    start_node = maze.start
    nodes_expanded = 0
    
    frontier = [start_node]     
    
    came_from: Dict[Pos, Pos] = {start_node: None}
    
    explored = {start_node}

    while frontier:
        current_node = frontier.pop()  
        nodes_expanded += 1

        if maze.goal_test(current_node):
            path = []
            temp = current_node
            while temp is not None:
                path.append(temp)
                temp = came_from[temp]
            path.reverse()
            cost = len(path) - 1
            return path, float(cost), nodes_expanded

        for action in maze.actions(current_node):
            neighbor = maze.result(current_node, action)
            if neighbor not in explored:
                explored.add(neighbor)
                came_from[neighbor] = current_node
                frontier.append(neighbor)   

    return None, None, nodes_expanded

if __name__ == '__main__':
    try:    
        maze_instance = Maze('../data/labirinto.txt')
        
        print("Labirinto carregado.")
        print(f"Início: {maze_instance.start}, Objetivo: {maze_instance.goal}\n")

        algorithms = {
            "BFS": bfs_search,
            "DFS": dfs_search,
            "A*": a_star_search,
            "Greedy Best-First Search": greedy_best_first_search
        }
        
        results = {}

        for name, func in algorithms.items():
            print(f"Executando {name}...")
            tracemalloc.start()
            start_time = time.perf_counter()
            
            path, cost, expanded_nodes = func(maze_instance)
            
            end_time = time.perf_counter()
            _, peak_mem = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            
            elapsed_time = end_time - start_time
            
            results[name] = {
                "path": path,
                "cost": cost,
                "expanded_nodes": expanded_nodes,
                "time": elapsed_time,
                "memory": peak_mem
            }

            print(f"{name} concluído em {elapsed_time:.6f} segundos.")
            print(f"Pico de memória ({name}): {peak_mem / 1024:.2f} KB")
            print(f"Nós expandidos ({name}): {expanded_nodes}\n")

        # --- Salvando todos os resultados ---
        output_filepath = '../data/results.txt'
        print(f"Salvando todos os resultados em {output_filepath}...")
        
        with open(output_filepath, 'w', encoding='utf-8') as f:
            for name, data in results.items():
                f.write(f"Algoritmo: {name}\n")
                if data["path"]:
                    f.write(f"Tempo de execução: {data['time']:.6f} segundos\n")
                    f.write(f"Pico de memória: {data['memory'] / 1024:.2f} KB\n")
                    f.write(f"Nós expandidos: {data['expanded_nodes']}\n")
                    f.write(f"Custo do caminho: {data['cost']}\n")
                    f.write(f"Nós no caminho: {len(data['path'])}\n")
                    f.write(f"Caminho: {data['path']}\n")
                else:
                    f.write("Nenhuma solução foi encontrada.\n")
                f.write("\n--------------------------------------------------\n\n")

        print("Resultados salvos com sucesso. ✅")

    except (FileNotFoundError, ValueError) as e:
        print(f"Ocorreu um erro: {e}")