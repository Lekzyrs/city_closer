import heapq
import random
from typing import Dict, List, Tuple, Set
from algorithms.base.router import BaseRouter


class ALTRouter(BaseRouter):
    """
    ALT Algorithm: A* with Landmarks and Triangle inequality
    Использует предварительно выбранные ориентиры для улучшенной эвристики
    """

    def __init__(self, graph: Dict[int, Dict[int, float]],
                 coordinates: Dict[int, Tuple[float, float]],
                 num_landmarks: int = 16):
        super().__init__(graph)
        self.coordinates = coordinates
        self.num_landmarks = num_landmarks
        self.landmarks = []
        self.dist_to_landmark = {}
        self.dist_from_landmark = {}

        self._select_landmarks()
        self._precompute_distances()

    def _select_landmarks(self):
        """Выбирает ориентиры (landmarks) в графе"""
        nodes = list(self.graph.keys())

        if len(nodes) <= self.num_landmarks:
            self.landmarks = nodes
        else:
            step = len(nodes) // self.num_landmarks
            self.landmarks = [nodes[i] for i in range(
                0, len(nodes), step)][:self.num_landmarks]

    def _precompute_distances(self):
        """Предвычисляет расстояния от/до каждого ориентира"""
        for landmark in self.landmarks:
            self.dist_from_landmark[landmark] = self._dijkstra_from_node(
                landmark)

            self.dist_to_landmark[landmark] = self._dijkstra_to_node(landmark)

    def _dijkstra_from_node(self, source: int) -> Dict[int, float]:
        """Запускает Дейкстру от узла source"""
        distances = {node: float('inf') for node in self.graph}
        distances[source] = 0
        pq = [(0, source)]

        while pq:
            dist, node = heapq.heappop(pq)
            if dist > distances[node]:
                continue

            for neighbor, weight in self.get_neighbors(node).items():
                new_dist = dist + weight
                if new_dist < distances[neighbor]:
                    distances[neighbor] = new_dist
                    heapq.heappush(pq, (new_dist, neighbor))

        return distances

    def _dijkstra_to_node(self, target: int) -> Dict[int, float]:
        """Запускает Дейкстру до узла target"""
        reverse_graph = {}
        for node, neighbors in self.graph.items():
            for neighbor, weight in neighbors.items():
                if neighbor not in reverse_graph:
                    reverse_graph[neighbor] = {}
                reverse_graph[neighbor][node] = weight

        distances = {node: float('inf') for node in self.graph}
        distances[target] = 0
        pq = [(0, target)]

        while pq:
            dist, node = heapq.heappop(pq)
            if dist > distances[node]:
                continue

            for neighbor, weight in reverse_graph.get(node, {}).items():
                new_dist = dist + weight
                if new_dist < distances[neighbor]:
                    distances[neighbor] = new_dist
                    heapq.heappush(pq, (new_dist, neighbor))

        return distances

    def _alt_heuristic(self, node: int, target: int) -> float:
        """
        Улучшенная эвристика с использованием ориентиров
        h(u, v) = max( |d(l, u) - d(l, v)|, d(u, l) - d(v, l) ) over all landmarks l
        """
        max_heuristic = 0.0

        for landmark in self.landmarks:
            h1 = abs(self.dist_from_landmark[landmark].get(node, 0) -
                     self.dist_from_landmark[landmark].get(target, 0))

            h2 = abs(self.dist_to_landmark[landmark].get(node, 0) -
                     self.dist_to_landmark[landmark].get(target, 0))

            heuristic = max(h1, h2)
            if heuristic > max_heuristic:
                max_heuristic = heuristic

        return max_heuristic

    def find_route(self, start: int, end: int) -> Tuple[List[int], float]:
        """
        Поиск пути с использованием ALT эвристики
        """
        if not self.validate_nodes(start, end):
            return [], float('inf')

        open_set = [(0, 0, start)]
        counter = 1

        g_score = {start: 0}
        f_score = {start: self._alt_heuristic(start, end)}

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

                    f = tentative_g + self._alt_heuristic(neighbor, end)
                    f_score[neighbor] = f

                    heapq.heappush(open_set, (f, counter, neighbor))
                    counter += 1

        return [], float('inf')
