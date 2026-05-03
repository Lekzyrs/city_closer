# 🌍 API маршрутизации по дорожной сети Москвы

## 📋 Описание проекта

Разработан API-сервис для построения оптимальных маршрутов по дорожной сети Москвы с использованием графовых алгоритмов поиска кратчайшего пути. Сервис загружает реальную дорожную сеть из OpenStreetMap и предоставляет REST API для маршрутизации.

### Основные возможности

-  Загрузка дорожного графа Москвы из OpenStreetMap
-  Поддержка 5 алгоритмов поиска кратчайшего пути
-  REST API с возвратом маршрута в формате GeoJSON
-  Кэширование графа для быстрой загрузки
-  Бенчмаркинг алгоритмов для выбора оптимального

## 🛠 Технологии

| Технология | Назначение |
|------------|------------|
| Python 3.10 | Язык программирования |
| OSMnx | Загрузка графов из OpenStreetMap |
| NetworkX | Работа с графами |
| FastAPI | REST API фреймворк |
| Uvicorn | ASGI сервер |
| Pydantic | Валидация данных |

## 📁 Структура проекта
city_closer/
├── route_service/
│ ├── algorithms/
│ │ ├── base/ # Базовые алгоритмы
│ │ │ ├── a_star.py # A* алгоритм
│ │ │ ├── bidirectional.py # Двунаправленный Дейкстра
│ │ │ └── router.py # Базовый класс
│ │ ├── shortest_path/ # Классические алгоритмы
│ │ │ └── dijkstra.py # Алгоритм Дейкстры
│ │ └── advanced/ # Продвинутые алгоритмы
│ │ ├── alt.py # ALT алгоритм
│ │ └── contraction_hierarchies.py # CH алгоритм
│ └── service/
│ ├── main.py # FastAPI приложение
│ ├── graph_loader.py # Загрузчик графа
│ ├── benchmark.py # Бенчмаркинг
│ └── enums.py # Перечисления
└── README.md


## 🚀 Установка и запуск

### 1. Клонирование репозитория

```bash
    git clone <repository-url>
    cd city_closer/route_service
```

### 2. Создание виртуального окружения
```bash
    python -m venv venv
    source venv/bin/activate  # Linux/Mac
    venv\Scripts\activate     # Windows
```

### 3. Установка зависимостей
```bash
    pip install -r requirements.txt
```

### 4. Запуск сервера
```bash
    cd route_service/service
    uvicorn main:app --reload --port 8000
```


### 5. Проверка работы
```bash
    # Проверка статуса
    curl http://localhost:8000/

    # Информация о сервисе
    curl http://localhost:8000/routing/v1/info

    # Построение маршрута
    curl -X POST http://localhost:8000/routing/v1/route \
    -H "Content-Type: application/json" \
    -d '{"ids": [46285457, 46285500, 46285530]}'
```