import sys
import os

current_file = os.path.abspath(__file__)
project_root = os.path.dirname(os.path.dirname(
    os.path.dirname(current_file)))
sys.path.insert(0, project_root)

from typing import Literal, Dict, Tuple
from algorithms.shortest_path.dijkstra import DijkstraRouter
from algorithms.base.a_star import AStarRouter
from algorithms.base.bidirectional import BidirectionalDijkstraRouter
from algorithms.advanced.contraction_hierarchies import ContractionHierarchies
from algorithms.advanced.alt import ALTRouter


class AlgorithmFactory:
    """Фабрика для создания экземпляров алгоритмов маршрутизации"""

    @staticmethod
    def create_algorithm(algorithm_type: str, graph: Dict, coordinates: Dict = None):
        """
        Создает экземпляр алгоритма по названию

        Args:
            algorithm_type: 'dijkstra', 'astar', 'bidirectional', 'ch', 'alt'
            graph: граф дорог
            coordinates: координаты узлов (нужны для A* и ALT)
        """
        if algorithm_type == 'dijkstra':
            return DijkstraRouter(graph)
        elif algorithm_type == 'astar':
            if coordinates is None:
                raise ValueError("A* requires coordinates")
            return AStarRouter(graph, coordinates)
        elif algorithm_type == 'bidirectional':
            return BidirectionalDijkstraRouter(graph)
        elif algorithm_type == 'ch':
            return ContractionHierarchies(graph)
        elif algorithm_type == 'alt':
            if coordinates is None:
                raise ValueError("ALT requires coordinates")
            return ALTRouter(graph, coordinates)
        else:
            raise ValueError(f"Unknown algorithm: {algorithm_type}")
