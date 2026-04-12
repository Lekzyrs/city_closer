def generate_instructions(path: List[int], graph, coordinates) -> List[Dict]:
    """
    Генерирует пошаговые инструкции для маршрута
    """
    instructions = []

    for i in range(len(path) - 1):
        current = path[i]
        next_node = path[i + 1]

        # Определяем угол поворота
        if i > 0:
            prev = path[i - 1]
            angle = calculate_turn_angle(prev, current, next_node, coordinates)
            maneuver = determine_maneuver(angle)
        else:
            maneuver = "start"

        # Вычисляем расстояние до следующего маневра
        distance = calculate_edge_distance(current, next_node, coordinates)

        instructions.append({
            "instruction": format_instruction(maneuver, distance),
            "distance": distance,
            "maneuver": maneuver,
            "point": coordinates[current]
        })

    # Добавляем инструкцию прибытия
    instructions.append({
        "instruction": "Вы прибыли в пункт назначения",
        "distance": 0,
        "maneuver": "arrive",
        "point": coordinates[path[-1]]
    })

    return instructions


def calculate_turn_angle(prev, curr, next_node, coordinates):
    """Вычисляет угол поворота между двумя отрезками пути"""
    # Упрощенная реализация
    return 0  # прямо


def determine_maneuver(angle):
    """Определяет тип маневра по углу поворота"""
    if angle < 30:
        return "continue"
    elif angle < 60:
        return "slight_right"
    elif angle < 120:
        return "turn_right"
    elif angle < 150:
        return "sharp_right"
    elif angle > 330:
        return "slight_left"
    elif angle > 300:
        return "turn_left"
    elif angle > 240:
        return "sharp_left"
    else:
        return "turn_around"


def format_instruction(maneuver, distance):
    """Форматирует инструкцию для пользователя"""
    instructions_map = {
        "start": "Начните движение",
        "continue": f"Продолжайте движение прямо {int(distance)} метров",
        "turn_right": f"Поверните направо через {int(distance)} метров",
        "turn_left": f"Поверните налево через {int(distance)} метров",
        "slight_right": f"Плавно поверните направо через {int(distance)} метров",
        "slight_left": f"Плавно поверните налево через {int(distance)} метров",
        "arrive": "Вы прибыли",
    }
    return instructions_map.get(maneuver, "Продолжайте движение")


def calculate_edge_distance(node1, node2, coordinates):
    """Вычисляет расстояние между двумя узлами"""
    coord1 = coordinates[node1]
    coord2 = coordinates[node2]

    lat_diff = (coord1[0] - coord2[0]) * 111000  # в метрах
    lon_diff = (coord1[1] - coord2[1]) * 85000   # в метрах

    return (lat_diff**2 + lon_diff**2) ** 0.5
