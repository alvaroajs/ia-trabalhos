# Relatório de IA - Busca em Labirinto

Este projeto implementa e compara quatro algoritmos de busca em espaço de estados para a resolução de problemas de labirinto. O objetivo é analisar o desempenho de algoritmos de busca não informada e informada em termos de tempo de execução, uso de memória, número de nós expandidos e optimalidade da solução.

Este código é o artefato de software para o primeiro trabalho prático da disciplina de Inteligência Artificial.

## Algoritmos Implementados

O projeto inclui a implementação dos seguintes algoritmos:

1.  **Busca em Largura (BFS):** Um algoritmo de busca não informada que garante o caminho mais curto em termos de número de passos.
2.  **Busca em Profundidade (DFS):** Um algoritmo de busca não informada eficiente em memória, mas que não garante a optimalidade.
3.  **Busca Gulosa (Greedy Best-First Search):** Um algoritmo de busca informada que utiliza uma heurística (Distância Euclidiana) para se guiar diretamente ao objetivo.
4.  **A* (A-Star):** Um algoritmo de busca informada que combina o custo do caminho ($g(n)$) com uma heurística admissível ($h(n)$) para garantir o caminho de menor custo total.

## Labirinto

Os labirintos estão na pasta `ia-trabalhos/trabalho1/data`, de modo que podem ser facilmente alterados a fim de obter os resultados que se deseja para cada cenário com os 4 tipos de algoritmos.

---

**Exemplo de Labirinto (`labirinto.txt`):**
``` 
S....
.###.
..#..
.###.
....G
```

## Requisitos (Requirements)

O projeto foi desenvolvido em Python e depende apenas de bibliotecas padrão. Não é necessária a instalação de pacotes externos.

* **Python 3.7** (ou superior)

Não há um arquivo `requirements.txt` necessário, pois todas as estruturas de dados utilizadas (como `collections.deque` para filas e `heapq` para filas de prioridade) fazem parte da biblioteca padrão do Python.

## Como Executar

Para executar os algoritmos de busca, utilize o script principal a partir da linha de comando, passando o caminho para o arquivo do labirinto e o nome do algoritmo desejado como argumentos.

### Sintaxe
```bash
python3 ia-trabalhos/trabalho1/src/*.py
```
- Com o *.py todos os arquivos .py serão executados de modo a gerar as tabelas para cada algoritimo
