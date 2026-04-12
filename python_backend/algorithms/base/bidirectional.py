# bidirectional.py - исправленная версия
import heapq
from typing import Dict, List, Tuple
from algorithms.base.router import BaseRouter


class BidirectionalDijkstraRouter(BaseRouter):
    """
    Двунаправленный алгоритм Дейкстры (оптимизированная версия)
    """

    def find_route(self, start: int, end: int) -> Tuple[List[int], float]:
        if not self.validate_nodes(start, end):
            return [], float('inf')

        # Прямой поиск
        forward_dist = {start: 0}
        forward_parent = {start: None}
        forward_heap = [(0, start)]
        forward_visited = set()

        # Обратный поиск
        backward_dist = {end: 0}
        backward_parent = {end: None}
        backward_heap = [(0, end)]
        backward_visited = set()

        best_length = float('inf')
        meeting_node = None

        while forward_heap and backward_heap:
            # Прямой шаг
            if forward_heap and forward_heap[0][0] < best_length:
                dist_f, node_f = heapq.heappop(forward_heap)

                if node_f in forward_visited:
                    continue
                forward_visited.add(node_f)

                # Проверка встречи
                if node_f in backward_dist:
                    total = dist_f + backward_dist[node_f]
                    if total < best_length:
                        best_length = total
                        meeting_node = node_f

                # Релаксация соседей (исправлено!)
                for neighbor, weight in self.get_neighbors(node_f).items():
                    if neighbor in forward_visited:
                        continue

                    new_dist = dist_f + weight
                    if neighbor not in forward_dist or new_dist < forward_dist[neighbor]:
                        forward_dist[neighbor] = new_dist
                        forward_parent[neighbor] = node_f
                        heapq.heappush(forward_heap, (new_dist, neighbor))

            # Обратный шаг (исправлено!)
            if backward_heap and backward_heap[0][0] < best_length:
                dist_b, node_b = heapq.heappop(backward_heap)

                if node_b in backward_visited:
                    continue
                backward_visited.add(node_b)

                # Проверка встречи
                if node_b in forward_dist:
                    total = forward_dist[node_b] + dist_b
                    if total < best_length:
                        best_length = total
                        meeting_node = node_b

                # Релаксация соседей в обратном направлении (исправлено!)
                for neighbor, weight in self.get_neighbors(node_b).items():
                    if neighbor in backward_visited:
                        continue

                    new_dist = dist_b + weight
                    if neighbor not in backward_dist or new_dist < backward_dist[neighbor]:
                        backward_dist[neighbor] = new_dist
                        backward_parent[neighbor] = node_b
                        heapq.heappush(backward_heap, (new_dist, neighbor))

        if meeting_node is not None:
            path = self._merge_paths(
                meeting_node, forward_parent, backward_parent)
            return path, best_length

        return [], float('inf')

    def _merge_paths(self, meeting_node: int,
                     forward_parent: Dict[int, int],
                     backward_parent: Dict[int, int]) -> List[int]:
        """Склеивает прямой и обратный пути"""
        # Путь от start до meeting_node
        forward_path = []
        node = meeting_node
        while node is not None:
            forward_path.append(node)
            node = forward_parent[node]
        forward_path.reverse()

        # Путь от meeting_node до end
        backward_path = []
        node = backward_parent.get(meeting_node)
        while node is not None:
            backward_path.append(node)
            node = backward_parent[node]

        return forward_path + backward_path
