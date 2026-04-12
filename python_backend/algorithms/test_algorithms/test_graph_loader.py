import sys
import os
import time

project_root = r'e:\Dev\misis\MRPO_LABS\city_closer'
sys.path.insert(0, project_root)
sys.path.insert(0, os.path.join(project_root, 'service'))
sys.path.insert(0, os.path.join(project_root, 'python_backend'))

from python_backend.service.graph_loader import MoscowGraphLoader


print("=== Testing Graph Loader ===\n")

# Тест 1: Drive (вся Москва)
print("1. Testing DRIVE network...")
start = time.time()
loader_drive = MoscowGraphLoader(network_type='drive')
graph_drive = loader_drive.load_graph(use_cache=False)
print(f"   ✅ Loaded in {time.time()-start:.2f}s")
print(f"   Nodes: {len(graph_drive)}")
print(f"   Sample node: {list(graph_drive.keys())[:3]}\n")

# Тест 2: Walk (только центр, 3 км радиус)
print("2. Testing WALK network (center, 3km radius)...")
start = time.time()
loader_walk = MoscowGraphLoader(network_type='walk')
graph_walk = loader_walk.load_graph(use_cache=False)
print(f"   ✅ Loaded in {time.time()-start:.2f}s")
print(f"   Nodes: {len(graph_walk)}")
if graph_walk:
    print(f"   Sample node: {list(graph_walk.keys())[:3]}\n")

# Тест 3: Bike (только центр, 3 км радиус)
print("3. Testing BIKE network (center, 3km radius)...")
start = time.time()
loader_bike = MoscowGraphLoader(network_type='bike')
graph_bike = loader_bike.load_graph(use_cache=False)
print(f"   ✅ Loaded in {time.time()-start:.2f}s")
print(f"   Nodes: {len(graph_bike)}")
if graph_bike:
    print(f"   Sample node: {list(graph_bike.keys())[:3]}\n")

print("="*50)
print("✅ All tests completed!")