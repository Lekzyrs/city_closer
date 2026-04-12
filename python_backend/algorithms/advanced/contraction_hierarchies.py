import heapq
from typing import Dict, List, Tuple, Set
from collections import defaultdict


class ContractionHierarchies:
    """
    Contraction Hierarchies - один из самых быстрых алгоритмов для маршрутизации
    Требует предварительной обработки графа (сжатия узлов)
    """

    def __init__(self, graph: Dict[int, Dict[int, float]]):
        self.original_graph = graph
        self.forward_graph = {}
        self.backward_graph = {}
        self.node_order = {}
        self.is_contracted = False

    def preprocess(self):
        """
        Предварительная обработка графа (сжатие узлов)
        Выполняется один раз при загрузке графа
        """
        print("Starting Contraction Hierarchies preprocessing...")

        self.forward_graph = {node: dict(
            neighbors) for node, neighbors in self.original_graph.items()}
        self.backward_graph = {node: {} for node in self.original_graph}

        for node, neighbors in self.original_graph.items():
            for neighbor, weight in neighbors.items():
                self.backward_graph[neighbor][node] = weight

        importance = self._calculate_importance()

        nodes_sorted = sorted(importance.keys(), key=lambda x: importance[x])

        order = 0
        for node in nodes_sorted:
            if self._should_contract(node):
                self._contract_node(node)
                self.node_order[node] = order
                order += 1

        self.is_contracted = True
        print(f"Preprocessing complete. Contracted {order} nodes.")

    def _calculate_importance(self) -> Dict[int, float]:
        """
        Вычисляет важность каждого узла для определения порядка контракции
        """
        importance = {}

        for node in self.original_graph:
            edge_diff = len(
                self.forward_graph[node]) + len(self.backward_graph[node])

            importance[node] = edge_diff + len(self.original_graph[node]) * 0.1

        return importance

    def _should_contract(self, node: int) -> bool:
        """Определяет, нужно ли контрактить узел"""
        return True

    def _contract_node(self, node: int):
        """
        Контрактит узел, удаляя его и добавляя короткие пути между его соседями
        """
        incoming = list(self.backward_graph[node].keys())
        outgoing = list(self.forward_graph[node].keys())

        for u in incoming:
            for v in outgoing:
                if u != v:
                    shortcut_weight = self.backward_graph[node][u] + \
                        self.forward_graph[node][v]

                    if not self._has_better_path(u, v, shortcut_weight):
                        self.forward_graph[u][v] = shortcut_weight
                        self.backward_graph[v][u] = shortcut_weight

        del self.forward_graph[node]
        del self.backward_graph[node]

        for u in incoming:
            del self.forward_graph[u][node]
            del self.backward_graph[node][u]

        for v in outgoing:
            del self.backward_graph[v][node]
            del self.forward_graph[node][v]

    def _has_better_path(self, u: int, v: int, weight: float) -> bool:
        """Проверяет, существует ли лучший путь между u и v"""
        if v in self.forward_graph.get(u, {}):
            return self.forward_graph[u][v] <= weight
        return False

    def query(self, start: int, end: int) -> Tuple[List[int], float]:
        """
        Поиск кратчайшего пути с использованием предобработанного графа
        """
        if not self.is_contracted:
            self.preprocess()

        forward_dist = {start: 0}
        forward_heap = [(0, start)]
        forward_parent = {}

        backward_dist = {end: 0}
        backward_heap = [(0, end)]
        backward_parent = {}

        best_distance = float('inf')
        meeting_node = None

        while forward_heap and backward_heap:
            if forward_heap:
                dist, node = heapq.heappop(forward_heap)
                if dist > forward_dist[node]:
                    continue

                if node in backward_dist:
                    total = dist + backward_dist[node]
                    if total < best_distance:
                        best_distance = total
                        meeting_node = node

                for neighbor, weight in self.forward_graph.get(node, {}).items():
                    if self.node_order.get(neighbor, -1) > self.node_order.get(node, -1):
                        new_dist = dist + weight
                        if neighbor not in forward_dist or new_dist < forward_dist[neighbor]:
                            forward_dist[neighbor] = new_dist
                            forward_parent[neighbor] = node
                            heapq.heappush(forward_heap, (new_dist, neighbor))

            if backward_heap:
                dist, node = heapq.heappop(backward_heap)
                if dist > backward_dist[node]:
                    continue

                if node in forward_dist:
                    total = forward_dist[node] + dist
                    if total < best_distance:
                        best_distance = total
                        meeting_node = node

                for neighbor, weight in self.backward_graph.get(node, {}).items():
                    if self.node_order.get(neighbor, -1) > self.node_order.get(node, -1):
                        new_dist = dist + weight
                        if neighbor not in backward_dist or new_dist < backward_dist[neighbor]:
                            backward_dist[neighbor] = new_dist
                            backward_parent[neighbor] = node
                            heapq.heappush(backward_heap, (new_dist, neighbor))

        if meeting_node is not None:
            path = self._reconstruct_ch_path(
                meeting_node, forward_parent, backward_parent)
            return path, best_distance

        return [], float('inf')

    def _reconstruct_ch_path(self, meeting_node: int,
                             forward_parent: Dict,
                             backward_parent: Dict) -> List[int]:
        """Восстанавливает полный путь из shortcut'ов"""
        path = [meeting_node]
        node = meeting_node
        while node in forward_parent:
            node = forward_parent[node]
            path.insert(0, node)

        node = meeting_node
        while node in backward_parent:
            node = backward_parent[node]
            path.append(node)

        return path
