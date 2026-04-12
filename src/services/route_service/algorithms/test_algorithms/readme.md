================================================================================
BENCHMARK STARTED at 2026-04-12 17:02:22
================================================================================
Graph size: 27437 nodes
Test pairs: 10
================================================================================
INFO:benchmark:Preparing algorithms...
INFO:benchmark:  Initializing dijkstra...
INFO:benchmark:  ✅ dijkstra ready
INFO:benchmark:  Initializing astar...
INFO:benchmark:  ✅ astar ready
INFO:benchmark:Prepared 2 algorithms
INFO:benchmark:Generating 10 test pairs...
INFO:benchmark:Generated 10 pairs

📊 Testing DIJKSTRA...
  ✅ Success: 10/10 (100.0%)
  ⏱️  Avg time: 35.052ms
  📏 Avg distance: 29269.9m

📊 Testing ASTAR...
  ✅ Success: 10/10 (100.0%)
  ⏱️  Avg time: 42.002ms
  📏 Avg distance: 29269.9m

================================================================================
BENCHMARK RESULTS
================================================================================

Algorithm       Success    Avg Time(ms)    Median(ms)      Avg Dist(m)    
--------------------------------------------------------------------------------
dijkstra        100.0    % 35.052          31.066          29269.9        
astar           100.0    % 42.002          34.853          29269.9        

================================================================================
RECOMMENDATION
================================================================================

🏆 BEST ALGORITHM: DIJKSTRA
   Avg time: 35.052 ms
   Success rate: 100.0%

✅ Benchmark completed successfully




$ python test_graph_loader.py
=== Testing Graph Loader ===

1. Testing DRIVE network...
Downloading Moscow graph with network_type='drive'...
Graph loaded: 27437 nodes, 58640 edges
   ✅ Loaded in 60.61s
   Nodes: 27437
   Sample node: [90058434, 90058438, 90058452]

2. Testing WALK network (center, 3km radius)...
Downloading Moscow graph with network_type='walk'...
Graph loaded: 547511 nodes, 1563165 edges
   ✅ Loaded in 423.13s
   Nodes: 547511
   Sample node: [90058438, 90058452, 90058453]

3. Testing BIKE network (center, 3km radius)...
Downloading Moscow graph with network_type='bike'...
Graph loaded: 241541 nodes, 567323 edges
   ✅ Loaded in 287.09s
   Nodes: 241541
   Sample node: [90058434, 90058438, 90058452]

==================================================
✅ All tests completed!


