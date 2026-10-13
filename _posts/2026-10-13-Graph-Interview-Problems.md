---
title: "Graph Interview Problems: Patterns, Steps and LeetCode Links"
layout: post
date: 2026-10-13 03:03:13
description: "Graph Interview Problems: Patterns, Steps and LeetCode Links"
tags:
  - Career
  - tech
categories:
  - tech
disqus_comments: false
rank: 1
featured: true
related_posts: true
---

## 1. Connected components and grid traversal

Loop over every node or cell; each time you find an unvisited one, `count++` and traverse its whole component. BFS and DFS both work for nearly all of these. (P) = LeetCode Premium.

|   |   |
|---|---|
|Problem|Approach|
|[Number of Provinces](https://leetcode.com/problems/number-of-provinces/)|1. Build an adjacency list from the matrix. 2. For each unvisited city, `count++`. 3. Traverse and mark everything reachable. **DFS:** recurse on neighbors. **BFS:** queue, mark on enqueue. Union-Find also works.|
|[Number of Islands](https://leetcode.com/problems/number-of-islands/)|Same template on a grid with 4 directions. Mark visited on entry, or flip `'1'` to `'0'`. **DFS** (recursive) and **BFS** (queue), both O(R·C).|
|[Flood Fill](https://leetcode.com/problems/flood-fill/)|Remember the original color and return early if it equals the new color. Recolor and spread to same-color neighbors. **DFS** or **BFS**.|
|[Max Area of Island](https://leetcode.com/problems/max-area-of-island/)|Island template, but the traversal returns the component size; keep the max. **DFS** is cleanest (return `1 + sum of neighbors`). **BFS** counts dequeues.|
|[Surrounded Regions](https://leetcode.com/problems/surrounded-regions/)|1. Start from every `'O'` on the border. 2. Mark everything reachable as safe (`'#'`). 3. Flip remaining `'O'` to `'X'`. 4. Restore `'#'` to `'O'`. **DFS** or **BFS** for the marking.|
|[Number of Enclaves](https://leetcode.com/problems/number-of-enclaves/)|Same as Surrounded Regions: traverse from border land cells, then count unvisited land cells. **DFS** or **BFS**.|
|[Pacific Atlantic Water Flow](https://leetcode.com/problems/pacific-atlantic-water-flow/)|Reverse the flow: traverse uphill from each ocean's border; the answer is the intersection of the two reachable sets. **DFS** or **BFS**.|
|[Keys and Rooms](https://leetcode.com/problems/keys-and-rooms/)|Traverse from room 0 and check every room was visited. **DFS** or **BFS**.|
|[Find if Path Exists in Graph](https://leetcode.com/problems/find-if-path-exists-in-graph/)|Reachability from source to destination. **DFS**, **BFS** or Union-Find.|

## 2. Shortest path in an unweighted graph or grid (BFS)

Use BFS from the source with distance kept in the queue or a `dist[]` array: the first time you reach a node is its shortest distance.

|   |   |
|---|---|
|Problem|Approach|
|[Rotting Oranges](https://leetcode.com/problems/rotting-oranges/)|1. Push **all** rotten oranges into the queue at once (multi-source). 2. Process level by level; each level is one minute. 3. If any fresh orange remains at the end, return -1. **BFS** required; a single DFS gives wrong times.|
|[01 Matrix](https://leetcode.com/problems/01-matrix/)|1. Seed the queue with all `0` cells at distance 0. 2. Expand outward. 3. A cell's first visit gives its distance to the nearest 0. **BFS** (multi-source).|
|[Shortest Path in Binary Matrix](https://leetcode.com/problems/shortest-path-in-binary-matrix/)|BFS with 8 directions. Return the level at which you reach the bottom-right cell.|
|[Word Ladder](https://leetcode.com/problems/word-ladder/)|1. Put the word list in a `HashSet`. 2. For each word, try all `W × 25` one-letter variations. 3. Enqueue those in the set and remove them so they aren't revisited. Return the level count. **BFS** (bidirectional BFS is a good follow-up).|
|[Word Ladder II](https://leetcode.com/problems/word-ladder-ii/)|BFS to compute levels and parents, then **DFS** backtracking to rebuild all shortest paths. Uses both.|
|[Shortest Bridge](https://leetcode.com/problems/shortest-bridge/)|1. **DFS** to find and mark the first island. 2. Put all its cells in the queue. 3. **BFS** outward until you hit the second island.|
|[Shortest Path in a Grid with Obstacles Elimination](https://leetcode.com/problems/shortest-path-in-a-grid-with-obstacles-elimination/)|BFS where the state is `(row, col, obstaclesLeft)`, and `visited` is keyed on the whole state.|

## 3. Cycle detection

The method depends on direction: undirected graphs use parent tracking or Union-Find, directed graphs need a 3-state DFS or Kahn's algorithm.

**Undirected: parent tracking.** Flag a cycle when you see a visited neighbor that isn't your parent.

- **DFS:** pass `parent` as an argument.
- **BFS:** store `(node, parent)` in the queue.
- **Union-Find:** if both endpoints of an edge are already connected, that edge closes a cycle.

|   |   |
|---|---|
|Problem|Approach|
|[Redundant Connection](https://leetcode.com/problems/redundant-connection/)|Union-Find is cleanest: return the edge whose endpoints are already connected.|
|[Graph Valid Tree](https://leetcode.com/problems/graph-valid-tree/) (P)|A tree means `E = V-1` and connected. Check with **DFS**, **BFS** or Union-Find.|

**Directed: parent tracking does not work**, because shared descendants look like cycles.

- **DFS:** 3-state array (`0` unvisited, `1` on the current path, `2` done). Reaching a node in state `1` means a cycle.
- **BFS:** Kahn's algorithm. If you process fewer than `V` nodes, there is a cycle.

|   |   |
|---|---|
|Problem|Approach|
|[Course Schedule](https://leetcode.com/problems/course-schedule/)|Directed cycle detection. Build edges `prereq → course`, then use the 3-state **DFS** or **BFS** (Kahn).|

## 4. Topological sort (directed acyclic graphs)

Reach for topological sort when the problem mentions order, prerequisites or dependencies. Kahn's algorithm (BFS) and post-order DFS both produce a valid order.

|   |   |
|---|---|
|Problem|Approach|
|[Course Schedule II](https://leetcode.com/problems/course-schedule-ii/)|**BFS (Kahn):** compute in-degrees, enqueue the zeros, pop while decrementing neighbors; the pop order is the answer if its length equals `V`. **DFS:** post-order push to a stack, reverse it, and use the 3-state check to catch cycles.|
|[Find Eventual Safe States](https://leetcode.com/problems/find-eventual-safe-states/)|**DFS:** a node is safe if it isn't on a cycle (state `2`). **BFS:** reverse all edges, run Kahn, and every node it processes is safe.|
|[Alien Dictionary](https://leetcode.com/problems/alien-dictionary/) (P)|1. Compare adjacent words; the first differing letter pair is an edge. 2. Watch for the invalid "abc before ab" case. 3. Topo sort. **BFS** or **DFS**; a cycle means the answer is `""`.|
|[Parallel Courses](https://leetcode.com/problems/parallel-courses/) (P)|Kahn's by levels; the level count is the number of semesters. **BFS**.|
|[All Paths From Source to Target](https://leetcode.com/problems/all-paths-from-source-to-target/)|DAG, so backtracking **DFS** with a path list. **BFS** works with paths held in the queue.|

Shortest path in a DAG (a GFG problem, not LeetCode): topo sort, then relax each node's edges in order. It runs in `O(V+E)` and handles negative weights.

## 5. Bipartite graphs (2-coloring)

A graph is bipartite exactly when it has no odd-length cycle. Both BFS and DFS can test it. Problems: [Is Graph Bipartite?](https://leetcode.com/problems/is-graph-bipartite/) and [Possible Bipartition](https://leetcode.com/problems/possible-bipartition/).

1. Color nodes `0` or `1`, starting a fresh traversal from every uncolored node (the graph can be disconnected).
2. Give each neighbor the opposite color.
3. If a neighbor already has your color, the graph is not bipartite.

## 6. Weighted shortest path

Pick the algorithm from the graph's properties: unit weights use BFS, a DAG uses topo sort plus relax, non-negative weights use Dijkstra, negative weights use Bellman-Ford, and all-pairs uses Floyd-Warshall.

|   |   |
|---|---|
|Problem|Algorithm and steps|
|[Network Delay Time](https://leetcode.com/problems/network-delay-time/)|**Dijkstra.** 1. Build a directed adjacency list. 2. Min-heap of `{node, dist}`. 3. Pop, skip stale entries (`d > dist[u]`), relax neighbors. 4. Answer is `max(dist)`, or -1 if any node is unreachable.|
|[Cheapest Flights Within K Stops](https://leetcode.com/problems/cheapest-flights-within-k-stops/)|**Bellman-Ford** limited to `K+1` rounds, using a copy of `dist` each round. Or **BFS** with a queue of `(node, cost, stops)`. Plain Dijkstra fails because the stop limit matters.|
|[Path With Minimum Effort](https://leetcode.com/problems/path-with-minimum-effort/)|Dijkstra on the grid where the "distance" is the max edge difference along the path. Binary search plus BFS also works.|
|[Swim in Rising Water](https://leetcode.com/problems/swim-in-rising-water/)|Same shape: Dijkstra with the max cell value along the path.|
|[Number of Ways to Arrive at Destination](https://leetcode.com/problems/number-of-ways-to-arrive-at-destination/)|Dijkstra plus a `ways[]` array. Equal distance adds the ways; a strictly shorter distance resets them.|
|[Find the City With the Smallest Number of Neighbors at a Threshold Distance](https://leetcode.com/problems/find-the-city-with-the-smallest-number-of-neighbors-at-a-threshold-distance/)|**Floyd-Warshall:** `dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])` for each `k`, then count nodes within the threshold. `O(V³)`.|

## 7. Union-Find (Disjoint Set Union)

Template: `find` with path compression and `union` by rank. If `find(u) == find(v)`, the two nodes are already connected.

|   |   |
|---|---|
|Problem|Approach|
|[Accounts Merge](https://leetcode.com/problems/accounts-merge/)|Union the emails belonging to the same account, then group by root. **DFS** over an email graph also works.|
|[Most Stones Removed](https://leetcode.com/problems/most-stones-removed-with-same-row-or-column/)|Treat rows and columns as nodes and union them for each stone. Answer is `stones - number of components`. **DFS** also works.|
|[Number of Operations to Make Network Connected](https://leetcode.com/problems/number-of-operations-to-make-network-connected/)|If `edges < n-1`, return -1. Otherwise the answer is `components - 1`. Union-Find, **DFS** or **BFS** to count components.|
|[Number of Connected Components in an Undirected Graph](https://leetcode.com/problems/number-of-connected-components-in-an-undirected-graph/) (P)|The Provinces template on an edge list.|
|[Making A Large Island](https://leetcode.com/problems/making-a-large-island/)|Label each island and record its size (**DFS** or Union-Find). Then try flipping each `0` and sum the sizes of the distinct neighboring islands, plus 1.|

## 8. Minimum spanning tree

Use an MST when the problem asks to connect everything at minimum total cost. Example: [Min Cost to Connect All Points](https://leetcode.com/problems/min-cost-to-connect-all-points/).

- **Kruskal:** sort edges by weight and add an edge if it joins two different components (Union-Find).
- **Prim:** start anywhere and use a min-heap of edges leaving the tree.

## 9. Advanced topics

|   |   |
|---|---|
|Problem|Approach|
|[Critical Connections in a Network](https://leetcode.com/problems/critical-connections-in-a-network/)|**Tarjan's bridges (DFS).** Track `disc[]` and `low[]`. Edge `u-v` is a bridge if `low[v] > disc[u]`.|
|[Clone Graph](https://leetcode.com/problems/clone-graph/)|`HashMap<Node, Node>` mapping each original to its clone; a map lookup is the visited check. **DFS** (recursive) or **BFS** (queue). Create the clone before recursing so cycles terminate.|
|[Minimum Height Trees](https://leetcode.com/problems/minimum-height-trees/)|Peel leaves layer by layer (Kahn-style on degrees) until 1 or 2 nodes remain. **BFS**.|
|[Evaluate Division](https://leetcode.com/problems/evaluate-division/)|Edges `a→b` with weight `value` and `b→a` with `1/value`; each query is a path product. **DFS** or **BFS**. Weighted Union-Find also works.|
|[Longest Increasing Path in a Matrix](https://leetcode.com/problems/longest-increasing-path-in-a-matrix/)|**DFS** with memoization. Kahn's on the "increasing" DAG is the **BFS** alternative.|
|[Reconstruct Itinerary](https://leetcode.com/problems/reconstruct-itinerary/)|Hierholzer's algorithm: **DFS** over sorted edges, post-order append, then reverse.|

Common follow-ups: strongly connected components (Kosaraju: DFS for finish order, reverse the graph, DFS in reverse finish order; each DFS tree is one SCC) and Dijkstra for the K-th shortest path.

## 10. Which template to reach for, and a practice order

Match the problem's wording to a template first, then work through the problems in the order below.

|   |   |
|---|---|
|If the problem says...|Reach for|
|"count groups", "connected"|DFS, BFS or Union-Find|
|"minimum steps", unweighted|BFS (multi-source if there are several starts)|
|"order", "prerequisites", "dependencies"|Topological sort|
|"can finish", "deadlock", "cycle"|Cycle detection (directed: 3-state or Kahn)|
|"two groups", "conflict"|Bipartite coloring|
|"cheapest", "fastest" with weights|Dijkstra, or Bellman-Ford if there is a stop limit or negative weights|
|"connect all at minimum cost"|MST|
|"all paths", "all solutions"|Backtracking DFS|
|"merge", "same group"|Union-Find|

Suggested order:

1. Number of Islands, Flood Fill, Number of Provinces
2. Rotting Oranges, 01 Matrix, Word Ladder
3. Course Schedule I and II, Is Graph Bipartite
4. Clone Graph, Surrounded Regions, Pacific Atlantic Water Flow
5. Network Delay Time, Cheapest Flights Within K Stops, Path With Minimum Effort
6. Redundant Connection, Accounts Merge, Min Cost to Connect All Points
7. Critical Connections, Alien Dictionary, Word Ladder II