import heapq
from typing import Dict, List, Tuple, Optional
from algorithms.base.router import BaseRouter


class DijkstraRouter(BaseRouter):
    """
    Классический алгоритм Дейкстры для поиска кратчайшего пути
    Сложность: O(E + V log V)
    """

    def find_route(self, start: int, end: int) -> Tuple[List[int], float]:
        """
        Находит кратчайший путь от start до end

        Алгоритм:
        1. Инициализируем расстояния (бесконечность для всех узлов)
        2. Начальному узлу присваиваем 0
        3. Используем priority queue для выбора узла с минимальным расстоянием
        4. Релаксируем всех соседей
        """
        if not self.validate_nodes(start, end):
            return [], float('inf')

        distances = {node: float('inf') for node in self.graph}
        distances[start] = 0
        came_from = {}

        pq = [(0, start)]
        visited = set()

        while pq:
            current_dist, current = heapq.heappop(pq)

            if current == end:
                path = self.reconstruct_path(came_from, current)
                return path, distances[current]

            if current in visited:
                continue
            visited.add(current)

            for neighbor, weight in self.get_neighbors(current).items():
                if neighbor in visited:
                    continue

                new_dist = current_dist + weight

                if new_dist < distances[neighbor]:
                    distances[neighbor] = new_dist
                    came_from[neighbor] = current
                    heapq.heappush(pq, (new_dist, neighbor))

        return [], float('inf')

    def find_all_distances(self, start: int) -> Dict[int, float]:
        """
        Находит расстояния от start до всех узлов
        Полезно для предварительных расчетов
        """
        distances = {node: float('inf') for node in self.graph}
        distances[start] = 0
        pq = [(0, start)]

        while pq:
            current_dist, current = heapq.heappop(pq)

            if current_dist > distances[current]:
                continue

            for neighbor, weight in self.get_neighbors(current).items():
                new_dist = current_dist + weight
                if new_dist < distances[neighbor]:
                    distances[neighbor] = new_dist
                    heapq.heappush(pq, (new_dist, neighbor))

        return distances
