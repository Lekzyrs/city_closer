from enum import Enum
from typing import Optional


class AlgorithmType(str, Enum):
    """Типы алгоритмов маршрутизации"""
    DIJKSTRA = "dijkstra"
    ASTAR = "astar"
    BIDIRECTIONAL = "bidirectional"
    CONTRACTION_HIERARCHIES = "ch"
    ALT = "alt"

    @classmethod
    def get_default(cls) -> "AlgorithmType":
        """Возвращает алгоритм по умолчанию"""
        return cls.ASTAR

    @classmethod
    def get_all(cls) -> list:
        """Возвращает все доступные алгоритмы"""
        return [member.value for member in cls]

    @classmethod
    def from_string(cls, value: str) -> Optional["AlgorithmType"]:
        """Создает enum из строки"""
        try:
            return cls(value.lower())
        except ValueError:
            return None

    def get_description(self) -> str:
        """Возвращает описание алгоритма"""
        descriptions = {
            AlgorithmType.DIJKSTRA: "Классический алгоритм Дейкстры. Медленный, но точный.",
            AlgorithmType.ASTAR: "A* с эвристикой. Оптимальный баланс скорости и точности.",
            AlgorithmType.BIDIRECTIONAL: "Двунаправленный Дейкстра. Быстрее классического.",
            AlgorithmType.CONTRACTION_HIERARCHIES: "Contraction Hierarchies. Очень быстрый после предобработки.",
            AlgorithmType.ALT: "ALT (A* с Landmarks). Улучшенная эвристика."
        }
        return descriptions.get(self, "Неизвестный алгоритм")
