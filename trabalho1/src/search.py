import heapq
from typing import List, Tuple, Dict, Optional
 
from maze import Maze, Pos
from heuristics import h_euclidean

def a_star_search(maze: Maze) -> Tuple[Optional[List[Pos]], Optional[float]]:
   
    start_node = maze.start
    goal_node = maze.goal
    
    frontier = [(h_euclidean(start_node, goal_node), start_node)]
    
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
                 
                priority = new_cost + h_euclidean(neighbor, goal_node)
                 
                heapq.heappush(frontier, (priority, neighbor))
                 
                came_from[neighbor] = current_node
  
    return None, None

def greedy_best_first_search(maze: Maze) -> Tuple[Optional[List[Pos]], Optional[float]]:
  
    start_node = maze.start
    goal_node = maze.goal
    
    frontier = [(h_euclidean(start_node, goal_node), start_node)]
    
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
                
                priority = h_euclidean(neighbor, goal_node)
                heapq.heappush(frontier, (priority, neighbor))
  
    return None, None
 
if __name__ == '__main__':
    try:    
        maze_instance = Maze('../data/labirinto.txt')
        
        print("Labirinto carregado. Iniciando busca A*...")
        print(f"Início: {maze_instance.start}, Objetivo: {maze_instance.goal}")

        a_star_solution_path, a_star_solution_cost = a_star_search(maze_instance)

        greedy_solution_path, greedy_solution_cost = greedy_best_first_search(maze_instance)
        output_filepath = '../data/results.txt'

        if a_star_solution_path:
            print("\nSolução encontrada! ✅")
            print(f"Custo do caminho: {a_star_solution_cost}")
            print(f"Salvando resultados em {output_filepath}...")

            a_star_result_content = (
                f"Algoritmo: A*\n"
                f"Custo do caminho: {a_star_solution_cost}\n"
                f"Caminho ({len(a_star_solution_path)} nós):\n"
                f"{a_star_solution_path}\n"
            )

            greedy_result_content = (
                f"Algoritmo: Greedy Best-First Search\n"
                f"Custo do caminho: {greedy_solution_cost}\n"
                f"Caminho ({len(greedy_solution_path)} nós):\n"
                f"{greedy_solution_path}\n"
            )
            
            with open(output_filepath, 'w', encoding='utf-8') as f:
                f.write(a_star_result_content)
                f.write("\n")
                f.write(greedy_result_content)

            
            print("Resultados salvos com sucesso.")

        else:
            print("\nNenhuma solução foi encontrada. ❌")
            with open(output_filepath, 'w', encoding='utf-8') as f:
                f.write("Nenhuma solução foi encontrada pelo algoritmo A*.\n")

    except (FileNotFoundError, ValueError) as e:
        print(f"Ocorreu um erro: {e}")