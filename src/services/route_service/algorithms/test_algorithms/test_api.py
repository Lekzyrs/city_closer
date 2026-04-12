
import requests
import sys
import os
project_root = r'e:\Dev\misis\MRPO_LABS\city_closer'
sys.path.insert(0, project_root)
sys.path.insert(0, os.path.join(project_root, 'service'))
from python_backend.service.graph_loader import MoscowGraphLoader

BASE_URL = "http://localhost:8000"


def get_real_node_ids():
    """Получает реальные ID узлов из графа"""
    try:
        loader = MoscowGraphLoader(network_type='drive')
        graph = loader.load_graph(use_cache=True)
        nodes = list(graph.keys())

        if len(nodes) < 3:
            print("⚠️  Недостаточно узлов в графе")
            return None

        # Берем 3 случайных узла
        import random
        test_ids = random.sample(nodes, min(3, len(nodes)))
        print(f"✅ Используем реальные ID узлов: {test_ids}")
        return test_ids

    except Exception as e:
        print(f"❌ Ошибка загрузки графа: {e}")
        return None


def test_api():
    """Тестирует API с реальными ID"""

    print("=== Testing FastAPI Endpoints ===\n")

    # 1. Проверка статуса
    print("1. Проверка сервера...")
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            print(f"   ✅ Сервер работает")
            print(f"   {response.json()}")
        else:
            print(f"   ❌ Ошибка: {response.status_code}")
            return
    except Exception as e:
        print(f"   ❌ Сервер не доступен: {e}")
        print("   Запустите сервер: uvicorn main:app --reload --port 8000")
        return

    # 2. Получение информации
    print("\n2. Информация о графе...")
    try:
        response = requests.get(f"{BASE_URL}/routing/v1/info")
        if response.status_code == 200:
            info = response.json()
            print(f"   ✅ Узлов: {info['graph']['nodes']}")
            print(f"   ✅ Ребер: {info['graph']['edges']}")
            print(f"   ✅ Алгоритм: {info['algorithm']}")
        else:
            print(f"   ❌ Ошибка: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Ошибка: {e}")

    # 3. Получаем реальные ID узлов
    print("\n3. Получение реальных ID узлов...")
    test_ids = get_real_node_ids()

    if not test_ids:
        print("   ❌ Не удалось получить ID узлов")
        return

    # 4. Тестирование маршрута
    print(f"\n4. Тестирование маршрута с ID: {test_ids}")

    payload = {"ids": test_ids}

    try:
        response = requests.post(
            f"{BASE_URL}/routing/v1/route",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=30
        )

        if response.status_code == 200:
            route = response.json()
            props = route['properties']
            print(f"   ✅ Маршрут построен!")
            print(f"   📏 Расстояние: {props['total_distance_km']} км")
            print(
                f"   📍 Точек в маршруте: {len(route['geometry']['coordinates'])}")
            print(
                f"   ⏱️  Время обработки: {props.get('processing_time_ms', 'N/A')} мс")

            # Показываем первые 5 координат
            coords = route['geometry']['coordinates'][:5]
            print(f"   🗺️  Первые координаты: {coords}")

        elif response.status_code == 404:
            print(f"   ⚠️  Узел не найден: {response.json()}")
        else:
            print(f"   ❌ Ошибка: {response.status_code}")
            print(f"   {response.json()}")

    except requests.exceptions.Timeout:
        print(f"   ⚠️  Таймаут (маршрут слишком длинный)")
    except Exception as e:
        print(f"   ❌ Ошибка: {e}")

    # 5. Тестирование информации об узле
    print(f"\n5. Информация об узле {test_ids[0]}...")
    try:
        response = requests.get(f"{BASE_URL}/routing/v1/node/{test_ids[0]}")
        if response.status_code == 200:
            node_info = response.json()
            print(f"   ✅ Узел найден")
            print(f"   📍 Координаты: {node_info['coordinates']}")
            print(f"   🔗 Степень: {node_info['degree']}")
        else:
            print(f"   ❌ Ошибка: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Ошибка: {e}")

    print("\n" + "="*50)
    print("✅ Тестирование завершено")


if __name__ == "__main__":
    test_api()
