import sys
import os

current_file = os.path.abspath(__file__)
project_root = os.path.dirname(os.path.dirname(
    os.path.dirname(current_file)))
sys.path.insert(0, project_root)

import time
import random
from typing import List, Tuple, Dict, Optional
import statistics
import logging
from datetime import datetime

from algorithms.shortest_path.dijkstra import DijkstraRouter
from algorithms.base.a_star import AStarRouter
from algorithms.base.bidirectional import BidirectionalDijkstraRouter
from algorithms.advanced.contraction_hierarchies import ContractionHierarchies
from algorithms.advanced.alt import ALTRouter

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def setup_paths():
    current_file = os.path.abspath(__file__)
    current_dir = os.path.dirname(current_file)

    possible_roots = [
        current_dir,
        os.path.dirname(current_dir),
        os.path.dirname(os.path.dirname(current_dir)),
        os.path.dirname(os.path.dirname(os.path.dirname(current_dir))),
    ]

    for root in possible_roots:
        if os.path.exists(os.path.join(root, 'algorithms')):
            sys.path.insert(0, root)
            print(f"✅ Added to path: {root}")
            return root
    return None


PROJECT_ROOT = setup_paths()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AlgorithmBenchmark:
    """Бенчмарк для сравнения алгоритмов маршрутизации"""

    def __init__(self, graph: Dict[int, Dict[int, float]],
                 coordinates: Dict[int, Tuple[float, float]]):
        self.graph = graph
        self.coordinates = coordinates
        self.results = {}
        self.algorithms = {}

    def prepare_algorithms(self, algorithms_to_prepare: List[str] = None,
                           skip_ch_preprocessing: bool = False):
        """
        Подготавливает алгоритмы к тестированию
        
        Args:
            algorithms_to_prepare: список алгоритмов
            skip_ch_preprocessing: пропустить предобработку CH (если уже есть)
        """
        logger.info("Preparing algorithms...")

        available = {
            'dijkstra': lambda: DijkstraRouter(self.graph),
            'astar': lambda: AStarRouter(self.graph, self.coordinates),
            'bidirectional': lambda: BidirectionalDijkstraRouter(self.graph),
            'alt': lambda: ALTRouter(self.graph, self.coordinates, num_landmarks=8),
            'ch': lambda: ContractionHierarchies(self.graph)
        }

        if algorithms_to_prepare is None:
            algorithms_to_prepare = list(available.keys())

        for name in algorithms_to_prepare:
            if name in available:
                try:
                    logger.info(f"  Initializing {name}...")
                    self.algorithms[name] = available[name]()

                    if name == 'ch':
                        if skip_ch_preprocessing:
                            logger.info(
                                "    CH already preprocessed, skipping...")
                        else:
                            logger.info(
                                "    ⚠️  Preprocessing Contraction Hierarchies...")
                            logger.info(
                                "    This may take 5-30 minutes for Moscow graph!")
                            start_time = time.time()

                            try:
                                self.algorithms[name].preprocess()
                                logger.info(
                                    f"    ✅ CH preprocessing completed in {time.time() - start_time:.2f}s")

                                self._save_ch_to_cache()

                            except Exception as e:
                                logger.error(
                                    f"    ❌ CH preprocessing failed: {e}")
                                self.algorithms[name] = None
                    else:
                        logger.info(f"  ✅ {name} ready")

                except Exception as e:
                    logger.error(f"  ❌ Failed to initialize {name}: {e}")
                    self.algorithms[name] = None
            else:
                logger.warning(f"  ⚠️  Algorithm {name} not available")

        logger.info(
            f"Prepared {len([a for a in self.algorithms.values() if a is not None])} algorithms")

    def _save_ch_to_cache(self, cache_file: str = 'ch_preprocessed.pkl'):
        """Сохраняет предобработанный CH в кэш"""
        import pickle
        try:
            ch = self.algorithms.get('ch')
            if ch and ch.is_contracted:
                with open(cache_file, 'wb') as f:
                    pickle.dump({
                        'forward_graph': ch.forward_graph,
                        'backward_graph': ch.backward_graph,
                        'node_order': ch.node_order,
                        'is_contracted': ch.is_contracted
                    }, f)
                logger.info(
                    f"    💾 CH preprocessed data saved to {cache_file}")
        except Exception as e:
            logger.warning(f"    Failed to save CH cache: {e}")

    def _load_ch_from_cache(self, cache_file: str = 'ch_preprocessed.pkl') -> bool:
        """Загружает предобработанный CH из кэша"""
        import pickle
        import os

        if not os.path.exists(cache_file):
            return False

        try:
            with open(cache_file, 'rb') as f:
                data = pickle.load(f)

            ch = self.algorithms.get('ch')
            if ch:
                ch.forward_graph = data['forward_graph']
                ch.backward_graph = data['backward_graph']
                ch.node_order = data['node_order']
                ch.is_contracted = data['is_contracted']
                logger.info(f"    ✅ CH loaded from cache: {cache_file}")
                return True
        except Exception as e:
            logger.warning(f"    Failed to load CH cache: {e}")

        return False

    def generate_test_pairs(self, num_pairs: int = 100) -> List[Tuple[int, int]]:
        """Генерирует случайные пары узлов"""
        nodes = list(self.graph.keys())

        if len(nodes) < 2:
            logger.error("Not enough nodes in graph")
            return []

        pairs = []
        attempts = 0
        max_attempts = num_pairs * 10

        logger.info(f"Generating {num_pairs} test pairs...")

        while len(pairs) < num_pairs and attempts < max_attempts:
            start = random.choice(nodes)
            end = random.choice(nodes)

            if start != end:
                pairs.append((start, end))
            attempts += 1

        logger.info(f"Generated {len(pairs)} pairs")
        return pairs

    def run_single_test(self, algorithm_name: str, start: int, end: int, timeout_seconds: int = 60):
        """Запускает один тест для алгоритма"""
        algorithm = self.algorithms.get(algorithm_name)

        if algorithm is None:
            return None, None, 0.0

        try:
            start_time = time.perf_counter()

            if hasattr(algorithm, 'query'):
                path, distance = algorithm.query(start, end)
            elif hasattr(algorithm, 'find_route'):
                path, distance = algorithm.find_route(start, end)
            else:
                return None, None, 0.0

            elapsed = time.perf_counter() - start_time

            return path, distance, elapsed

        except Exception as e:
            logger.debug(f"Error in {algorithm_name}: {e}")
            return None, None, 0.0

    def run_benchmark(self, num_pairs: int = 50,
                      algorithms_to_test: List[str] = None,
                      include_ch: bool = False,
                      ch_preprocess_once: bool = True) -> Dict:
        """
        Запускает бенчмарк
        
        Args:
            num_pairs: количество тестовых пар
            algorithms_to_test: список алгоритмов
            include_ch: включить CH (требует предобработки)
            ch_preprocess_once: предобработать CH один раз (True) или каждый тест (False)
        """
        print("\n" + "="*80)
        print(
            f"BENCHMARK STARTED at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*80)
        print(f"Graph size: {len(self.graph)} nodes")
        print(f"Test pairs: {num_pairs}")
        print("="*80)

        if algorithms_to_test is None:
            algorithms_to_test = ['dijkstra', 'astar', 'bidirectional']
            if include_ch:
                algorithms_to_test.append('ch')

        if include_ch and 'ch' in algorithms_to_test:
            self.algorithms = {}

            for name in algorithms_to_test:
                if name != 'ch':
                    try:
                        if name == 'dijkstra':
                            self.algorithms[name] = DijkstraRouter(self.graph)
                        elif name == 'astar':
                            self.algorithms[name] = AStarRouter(
                                self.graph, self.coordinates)
                        elif name == 'bidirectional':
                            self.algorithms[name] = BidirectionalDijkstraRouter(
                                self.graph)
                        elif name == 'alt':
                            self.algorithms[name] = ALTRouter(
                                self.graph, self.coordinates)
                        logger.info(f"✅ {name} ready")
                    except Exception as e:
                        logger.error(f"❌ Failed to initialize {name}: {e}")
                        self.algorithms[name] = None

            self.algorithms['ch'] = ContractionHierarchies(self.graph)

            if not self._load_ch_from_cache():
                if ch_preprocess_once:
                    logger.info("⏳ Preprocessing CH (one time operation)...")
                    start_time = time.time()
                    self.algorithms['ch'].preprocess()
                    logger.info(
                        f"✅ CH preprocessing completed in {time.time() - start_time:.2f}s")
                    self._save_ch_to_cache()
                else:
                    logger.info(
                        "CH will be preprocessed for each test (slow!)")
        else:
            self.prepare_algorithms(algorithms_to_test)

        test_pairs = self.generate_test_pairs(num_pairs)

        if not test_pairs:
            print("❌ No test pairs generated!")
            return {}

        results = {}

        for name in [a for a in algorithms_to_test if a in self.algorithms]:
            if self.algorithms.get(name) is None:
                continue

            print(f"\n📊 Testing {name.upper()}...")

            times = []
            distances = []
            successful = 0

            for start, end in test_pairs:
                path, distance, elapsed = self.run_single_test(
                    name, start, end)

                if path and distance is not None:
                    times.append(elapsed)
                    distances.append(distance)
                    successful += 1

            if times:
                results[name] = {
                    'avg_time_ms': statistics.mean(times) * 1000,
                    'median_time_ms': statistics.median(times) * 1000,
                    'min_time_ms': min(times) * 1000,
                    'max_time_ms': max(times) * 1000,
                    'std_time_ms': statistics.stdev(times) * 1000 if len(times) > 1 else 0,
                    'success_rate': successful / len(test_pairs) * 100,
                    'avg_distance_m': statistics.mean(distances),
                    'total_tests': len(test_pairs),
                    'successful': successful
                }

                print(
                    f"  ✅ Success: {successful}/{len(test_pairs)} ({results[name]['success_rate']:.1f}%)")
                print(f"  ⏱️  Avg time: {results[name]['avg_time_ms']:.3f}ms")
                print(
                    f"  📏 Avg distance: {results[name]['avg_distance_m']:.1f}m")
            else:
                results[name] = {'error': 'No successful routes'}
                print(f"  ❌ No successful routes")

        self.results = results
        return results

    def print_results(self):
        """Выводит результаты"""
        print("\n" + "="*80)
        print("BENCHMARK RESULTS")
        print("="*80)

        valid_results = [(name, data) for name,
                         data in self.results.items() if 'avg_time_ms' in data]

        if not valid_results:
            print("No valid results")
            return None

        valid_results.sort(key=lambda x: x[1]['avg_time_ms'])

        print(
            f"\n{'Algorithm':<15} {'Success':<10} {'Avg Time(ms)':<15} {'Median(ms)':<15} {'Avg Dist(m)':<15}")
        print("-"*80)

        for name, data in valid_results:
            print(f"{name:<15} {data['success_rate']:<9.1f}% {data['avg_time_ms']:<15.3f} "
                  f"{data['median_time_ms']:<15.3f} {data['avg_distance_m']:<15.1f}")

        print("\n" + "="*80)
        print("RECOMMENDATION")
        print("="*80)

        best = valid_results[0][0]
        best_data = valid_results[0][1]

        print(f"\n🏆 BEST ALGORITHM: {best.upper()}")
        print(f"   Avg time: {best_data['avg_time_ms']:.3f} ms")
        print(f"   Success rate: {best_data['success_rate']:.1f}%")

        if 'ch' in [n for n, _ in valid_results]:
            ch_data = next((d for n, d in valid_results if n == 'ch'), None)
            if ch_data and ch_data['avg_time_ms'] < 10:
                print(
                    f"\n💡 Note: CH is extremely fast ({ch_data['avg_time_ms']:.3f}ms per query)")
                print(
                    "   but requires long preprocessing (5-30 minutes) for the first run")

        return best


class CHBenchmark:
    """Специальный бенчмарк для Contraction Hierarchies"""

    def __init__(self, graph: Dict[int, Dict[int, float]]):
        self.graph = graph
        self.ch = None

    def preprocess_and_save(self, cache_file: str = 'ch_preprocessed.pkl'):
        """Предобрабатывает CH и сохраняет в кэш"""
        import pickle

        print("="*60)
        print("CONTRACTION HIERARCHIES PREPROCESSING")
        print("="*60)
        print(f"Graph size: {len(self.graph)} nodes")
        print("This may take 5-30 minutes depending on graph size...")
        print("="*60)

        start_time = time.time()

        self.ch = ContractionHierarchies(self.graph)
        self.ch.preprocess()

        elapsed = time.time() - start_time

        print(
            f"\n✅ Preprocessing completed in {elapsed:.2f}s ({elapsed/60:.2f} minutes)")

        with open(cache_file, 'wb') as f:
            pickle.dump({
                'forward_graph': self.ch.forward_graph,
                'backward_graph': self.ch.backward_graph,
                'node_order': self.ch.node_order,
                'is_contracted': self.ch.is_contracted
            }, f)

        print(f"💾 Saved to {cache_file}")

        return self.ch

    def load_from_cache(self, cache_file: str = 'ch_preprocessed.pkl') -> bool:
        """Загружает предобработанный CH из кэша"""
        import pickle
        import os

        if not os.path.exists(cache_file):
            print(f"❌ Cache file {cache_file} not found")
            return False

        try:
            with open(cache_file, 'rb') as f:
                data = pickle.load(f)

            self.ch = ContractionHierarchies(self.graph)
            self.ch.forward_graph = data['forward_graph']
            self.ch.backward_graph = data['backward_graph']
            self.ch.node_order = data['node_order']
            self.ch.is_contracted = data['is_contracted']

            print(f"✅ CH loaded from cache: {cache_file}")
            return True

        except Exception as e:
            print(f"❌ Failed to load CH cache: {e}")
            return False

    def run_queries(self, num_queries: int = 1000) -> Dict:
        """Запускает множество запросов для измерения производительности"""
        if not self.ch or not self.ch.is_contracted:
            print("❌ CH not preprocessed. Run preprocess_and_save() first")
            return {}

        nodes = list(self.graph.keys())

        queries = []
        for _ in range(num_queries):
            start = random.choice(nodes)
            end = random.choice(nodes)
            while start == end:
                end = random.choice(nodes)
            queries.append((start, end))

        times = []
        successful = 0

        print(f"\nRunning {num_queries} CH queries...")

        for start, end in queries:
            start_time = time.perf_counter()
            path, distance = self.ch.query(start, end)
            elapsed = time.perf_counter() - start_time

            if path:
                times.append(elapsed)
                successful += 1

        if times:
            results = {
                'total_queries': num_queries,
                'successful': successful,
                'success_rate': successful / num_queries * 100,
                'avg_time_ms': statistics.mean(times) * 1000,
                'median_time_ms': statistics.median(times) * 1000,
                'min_time_ms': min(times) * 1000,
                'max_time_ms': max(times) * 1000,
                'throughput_qps': successful / sum(times) if times else 0
            }

            print(f"\n📊 CH Performance:")
            print(f"   Success rate: {results['success_rate']:.1f}%")
            print(f"   Avg time: {results['avg_time_ms']:.3f} ms")
            print(
                f"   Throughput: {results['throughput_qps']:.1f} queries/sec")

            return results

        return {}


if __name__ == "__main__":
    from route_service.graph_loader import MoscowGraphLoader

    loader = MoscowGraphLoader(network_type='drive')
    graph = loader.load_graph(use_cache=True)
    coords = loader.get_coordinates()

    #Быстрый тест без CH
    print("\n" + "="*60)
    print("OPTION 1: Quick benchmark (without CH)")
    print("="*60)
    benchmark = AlgorithmBenchmark(graph, coords)
    results = benchmark.run_benchmark(
        num_pairs=10,
        algorithms_to_test=['dijkstra', 'astar']
    )
    benchmark.print_results()

    # Тест с CH (требует времени на предобработку)
    print("\n" + "="*60)
    print("OPTION 2: CH benchmark (requires preprocessing)")
    print("="*60)

    ch_bench = CHBenchmark(graph)

    if not ch_bench.load_from_cache():
        answer = input(
            "Preprocess CH? This will take 5-30 minutes. Continue? (y/n): ")
        if answer.lower() == 'y':
            ch_bench.preprocess_and_save()
        else:
            print("Skipping CH benchmark")
            exit()

    ch_results = ch_bench.run_queries(num_queries=100)
