import math
from typing import Tuple, Dict


class Heuristics:
    """Коллекция эвристических функций для A* и других алгоритмов"""

    @staticmethod
    def euclidean_distance(coord1: Tuple[float, float],
                           coord2: Tuple[float, float]) -> float:
        """
        Евклидово расстояние между двумя точками (в километрах)
        """
        lat1, lon1 = coord1
        lat2, lon2 = coord2

        # Приближенное преобразование градусов в километры
        lat_diff = (lat1 - lat2) * 111  # 1 градус широты ≈ 111 км
        # 1 градус долготы ≈ 85 км на широте Москвы
        lon_diff = (lon1 - lon2) * 85

        return math.sqrt(lat_diff**2 + lon_diff**2)

    @staticmethod
    def haversine_distance(coord1: Tuple[float, float],
                           coord2: Tuple[float, float]) -> float:
        """
        Точное расстояние по формуле гаверсинуса (в километрах)
        """
        lat1, lon1 = math.radians(coord1[0]), math.radians(coord1[1])
        lat2, lon2 = math.radians(coord2[0]), math.radians(coord2[1])

        dlat = lat2 - lat1
        dlon = lon2 - lon1

        a = math.sin(dlat/2)**2 + math.cos(lat1) * \
            math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.asin(math.sqrt(a))

        r = 6371  # Радиус Земли в километрах
        return r * c

    @staticmethod
    def manhattan_distance(coord1: Tuple[float, float],
                           coord2: Tuple[float, float]) -> float:
        """
        Манхэттенское расстояние (для городских условий)
        """
        lat1, lon1 = coord1
        lat2, lon2 = coord2

        return abs(lat1 - lat2) * 111 + abs(lon1 - lon2) * 85
