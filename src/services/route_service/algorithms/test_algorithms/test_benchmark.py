from benchmark import AlgorithmBenchmark
import sys
import os
project_root = r'e:\Dev\misis\MRPO_LABS\city_closer'
sys.path.insert(0, project_root)
sys.path.insert(0, os.path.join(project_root, 'service'))

from python_backend.service.graph_loader import MoscowGraphLoader

print("=== Testing Benchmark ===")

print("Loading small graph...")
loader = MoscowGraphLoader(network_type='drive')
graph = loader.load_graph(use_cache=True)
coordinates = loader.get_coordinates()

benchmark = AlgorithmBenchmark(graph, coordinates)

print("\nRunning benchmark with 10 random pairs...")
results = benchmark.run_benchmark(
    num_pairs=10,  algorithms_to_test=['dijkstra', 'astar'])

benchmark.print_results()

print("\n✅ Benchmark completed successfully")
