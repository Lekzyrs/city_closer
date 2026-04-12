from abc import ABC, abstractmethod
from typing import Dict, List, Tuple, Optional, Any
import heapq


class BaseRouter(ABC):
    """
    Абстрактный базовый класс для всех алгоритмов маршрутизации
    """

    def __init__(self, graph: Dict[int, Dict[int, float]]):
        """
        Args:
            graph: словарь вида {node_id: {neighbor_id: weight}}
        """
        self.graph = graph
        self.nodes_count = len(graph)

    @abstractmethod
    def find_route(self, start: int, end: int) -> Tuple[List[int], float]:
        """
        Находит оптимальный маршрут между двумя узлами
        
        Args:
            start: ID начального узла
            end: ID конечного узла
            
        Returns:
            Tuple[List[int], float]: (путь в виде списка узлов, общая стоимость)
        """
        pass

    def reconstruct_path(self, came_from: Dict[int, int], current: int) -> List[int]:
        """
        Восстанавливает путь из словаря предков
        
        Args:
            came_from: словарь {узел: предыдущий_узел}
            current: конечный узел
            
        Returns:
            List[int]: путь от начала до конца
        """
        path = [current]
        while current in came_from:
            current = came_from[current]
            path.append(current)
        return path[::-1]

    def get_neighbors(self, node: int) -> Dict[int, float]:
        """Возвращает соседей узла"""
        return self.graph.get(node, {})

    def validate_nodes(self, start: int, end: int) -> bool:
        """Проверяет существование узлов в графе"""
        return start in self.graph and end in self.graph
