import sys
import os

current_file = os.path.abspath(__file__)
project_root = os.path.dirname(os.path.dirname(
    os.path.dirname(current_file)))
sys.path.insert(0, project_root)

import osmnx as ox
import networkx as nx
from typing import Dict, Tuple
import pickle


class MoscowGraphLoader:
    """Загрузчик графа Москвы с поддержкой разных типов маршрутизации"""

    def __init__(self, network_type: str = 'drive'):
        """
        Args:
            network_type: 'drive', 'walk', 'bike'
        """
        self.network_type = network_type
        self.graph = None
        self.node_coordinates = {}
        self.nx_graph = None

    def load_graph(self, use_cache: bool = True, cache_file: str = None) -> Dict[int, Dict[int, float]]:
        """
        Загружает граф Москвы

        Returns:
            Граф в формате {node: {neighbor: weight, ...}, ...}
        """
        if use_cache and cache_file:
            try:
                with open(cache_file, 'rb') as f:
                    self.graph, self.node_coordinates = pickle.load(f)
                print(f"Graph loaded from cache: {cache_file}")
                return self.graph
            except FileNotFoundError:
                print("Cache not found, downloading...")

        print(
            f"Downloading Moscow graph with network_type='{self.network_type}'...")

        try:
            G = ox.graph_from_place(
                'Moscow, Russia', network_type=self.network_type)
        except:
            print("Falling back to Moscow center...")
            G = ox.graph_from_bbox(
                55.85, 55.65, 37.7, 37.5, network_type=self.network_type)

        self.graph = {}
        self.node_coordinates = {}

        for node, data in G.nodes(data=True):
            self.graph[node] = {}
            self.node_coordinates[node] = (data['y'], data['x'])

        for u, v, data in G.edges(data=True):
            weight = data.get('length', 1.0)
            self.graph[u][v] = weight

            if not G.is_directed():
                self.graph[v][u] = weight

        self.nx_graph = G

        if cache_file:
            with open(cache_file, 'wb') as f:
                pickle.dump((self.graph, self.node_coordinates), f)
            print(f"Graph saved to cache: {cache_file}")

        print(
            f"Graph loaded: {len(self.graph)} nodes, {sum(len(n) for n in self.graph.values())} edges")
        return self.graph

    def get_coordinates(self) -> Dict[int, Tuple[float, float]]:
        """Возвращает координаты узлов"""
        return self.node_coordinates
