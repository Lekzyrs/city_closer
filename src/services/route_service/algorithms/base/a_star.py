import heapq
from typing import Dict, List, Tuple, Callable, Optional
from algorithms.base.router import BaseRouter


class AStarRouter(BaseRouter):
    """
    A* алгоритм с эвристикой для ускорения поиска
    Более эффективен чем Дейкстра, если есть хорошая эвристика
    """

    def __init__(self, graph: Dict[int, Dict[int, float]],
                 coordinates: Dict[int, Tuple[float, float]],
                 heuristic_func: Optional[Callable] = None):
        """
        Args:
            graph: граф дорог
            coordinates: координаты узлов {node_id: (lat, lon)}
            heuristic_func: функция эвристики (по умолчанию - евклидово расстояние)
        """
        super().__init__(graph)
        self.coordinates = coordinates
        self.heuristic_func = heuristic_func or self._euclidean_heuristic

    def _euclidean_heuristic(self, node_a: int, node_b: int) -> float:
        """
        Евклидово расстояние между узлами (в километрах)
        """
        lat1, lon1 = self.coordinates[node_a]
        lat2, lon2 = self.coordinates[node_b]

        lat_diff = lat1 - lat2
        lon_diff = lon1 - lon2

        return ((lat_diff * 111) ** 2 + (lon_diff * 85) ** 2) ** 0.5

    def _manhattan_heuristic(self, node_a: int, node_b: int) -> float:
        """
        Манхэттенское расстояние (для городских условий)
        """
        lat1, lon1 = self.coordinates[node_a]
        lat2, lon2 = self.coordinates[node_b]

        return abs(lat1 - lat2) * 111 + abs(lon1 - lon2) * 85

    def find_route(self, start: int, end: int) -> Tuple[List[int], float]:
        """
        Находит оптимальный путь с помощью A*
        
        f(n) = g(n) + h(n)
        где:
        - g(n): реальная стоимость от start до n
        - h(n): эвристическая оценка от n до end
        """
        if not self.validate_nodes(start, end):
            return [], float('inf')

        open_set = [(0, 0, start)]
        counter = 1

        g_score = {start: 0}
        f_score = {start: self.heuristic_func(start, end)}

        came_from = {}
        closed_set = set()

        while open_set:
            current_f, _, current = heapq.heappop(open_set)

            if current == end:
                path = self.reconstruct_path(came_from, current)
                return path, g_score[current]

            if current in closed_set:
                continue
            closed_set.add(current)

            for neighbor, weight in self.get_neighbors(current).items():
                if neighbor in closed_set:
                    continue

                tentative_g = g_score[current] + weight

                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g

                    f = tentative_g + self.heuristic_func(neighbor, end)
                    f_score[neighbor] = f

                    heapq.heappush(open_set, (f, counter, neighbor))
                    counter += 1

        return [], float('inf')

    def find_route_with_details(self, start: int, end: int) -> Dict:
        """
        Находит путь с дополнительной информацией (для отладки)
        """
        path, distance = self.find_route(start, end)

        return {
            'path': path,
            'distance': distance,
            'nodes_visited': len(self.graph) - len([n for n in self.graph if n not in closed_set]),
            'algorithm': 'A*'
        }
