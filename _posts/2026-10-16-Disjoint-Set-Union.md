---
title: "Disjoint Set Union-Study Guide"
layout: post
date: 2026-10-16 03:03:13
description: "Disjoint Set Union"
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
# Disjoint Set Union (Union-Find) study guide

Oct 17, 2026 · @Muneeb

A disjoint set union (DSU, also called union-find) is a tool for keeping track of groups. It can quickly tell you whether two things are in the same group, and quickly merge two groups into one. Each step is almost instant (technically O(α(n)), which is effectively constant). This guide explains the idea in plain words, shows traced runs of real code, and ends with a practice list with no solutions.

## What a DSU is

Think of friend groups. Every group has one captain. To check whether two people are in the same group, ask each one "who is your captain?" If the answers match, they are in the same group. To merge two groups, make one captain report to the other captain.

A DSU does exactly this with one array. `parent[x]` is the person that x reports to. A captain reports to themselves. If you keep following the parents, you always end at the captain. We call the captain the root.

Read the picture below from left to right. Eight people start alone. Four merges make pairs. Three more merges join everyone into one group. The whole structure is just the array `[0, 0, 0, 0, 0, 4, 4, 4]`, plus a `size[]` array that keeps the trees short.

&#91;embedded content: union-find forest · 8 elements, 7 merges\]

## The two operations and the Java class to memorise

`find(x)` walks up the parents until it reaches the captain (the root), and returns it. `union(a, b)` finds both captains and makes one report to the other. If both already have the same captain, they are already together, so nothing happens.

```
class DSU {
    int[] parent, size;
    int components;                       // number of sets right now

    DSU(int n) {
        parent = new int[n];
        size = new int[n];
        components = n;
        for (int i = 0; i < n; i++) { parent[i] = i; size[i] = 1; }
    }

    int find(int x) {                     // path compression
        if (parent[x] != x) parent[x] = find(parent[x]);
        return parent[x];
    }

    boolean union(int a, int b) {         // union by size
        int ra = find(a), rb = find(b);
        if (ra == rb) return false;       // already in the same set
        if (size[ra] < size[rb]) { int t = ra; ra = rb; rb = t; }
        parent[rb] = ra;
        size[ra] += size[rb];
        components--;
        return true;
    }

    boolean connected(int a, int b) { return find(a) == find(b); }
}
```

Every variant later in this guide is this same class with one extra array. `union` returns true if it merged two groups, and false if they were already together. That true or false answer is the trick behind cycle detection and Kruskal's algorithm below. This class was compiled and checked against a simple search on 2,000 random graphs.

## Why plain DSU is slow, and the two fixes

The plain version has a problem. If you call `union(0, 1)`, `union(1, 2)`, `union(2, 3)` and so on with no rules, you get one long chain. Then `find(0)` has to walk the whole chain. With 6 elements the array ends as `[1, 2, 3, 4, 5, 5]` and `find(0)` takes 5 steps. With a million elements it would take a million steps. Two small fixes solve this.

**Fix 1: path compression.** After `find` reaches the captain, it tells everyone it walked past: "your parent is now the captain directly." Next time, those people reach the captain in one step. After one `find(0)`, the chain `[1, 2, 3, 4, 4]` becomes `[4, 4, 4, 4, 4]`.

&#91;embedded content: path compression · chain of 5 before and after one find\]

**Fix 2: union by size.** When merging, put the smaller group under the bigger group's captain. A person only gets one level deeper when their group ends up inside one at least as big, so their group at least doubles. That means no one can be deeper than log2 n levels (about 20 levels for a million people).

&#91;embedded content: union by size · two ways to merge a 3-node and a 1-node tree\]

**Together**, the two fixes make every operation almost instant. The exact cost is O(α(n)) per operation on average, where α grows so slowly that it never goes above 4 for any realistic n ([cp-algorithms](https://cp-algorithms.com/data_structures/disjoint_set_union.html)). Either fix alone gives O(log n), which is also fast. The same page reports that choosing which tree goes under which by coin flip performs much worse than union by size.

## Types of DSU

There are two different questions here: how the structure is made fast (implementation variants), and what extra it remembers to answer a problem (problem variants).

**Implementation variants**

| Variant | `find` cost | What it does | When to use |
| --- | --- | --- | --- |
| Naive linking | O(n) worst case | Attach one root under the other with no rule | Never; a teaching baseline |
| Union by size | O(log n) | Hang the smaller tree under the larger | You want component sizes, or you need rollback |
| Union by rank | O(log n) | Hang the shorter tree (by a height bound) under the taller | Same cost as size; compression leaves rank as a stale bound |
| Path compression only | O(log n) amortised | Re-point every node on the find path at the root | Shortest code when speed is not critical |
| Path halving or splitting | Same bound as compression | Each visited node skips to its grandparent, in one iterative pass | You want an iterative `find` with no recursion |
| Compression + size or rank | O(α(n)) amortised | Both rules together | The default; use it unless a variant forbids it |

**Problem variants**

| Variant | Extra data | What it answers |
| --- | --- | --- |
| Plain | none | Same set? How many sets? Did this edge close a cycle? |
| Aggregate at the root | size, min, max or sum per root | Largest group, per-group totals |
| Non-integer or implicit nodes | HashMap ids, flattened grid index, a dummy node | Strings, emails, grid cells, "the boundary" |
| Parity | one bit per node | Bipartite check or odd cycle, online |
| Weighted (potential) | offset to the parent | Differences or ratios inside a group, and contradictions |
| Offline, sorted or reversed | none; the processing order is the trick | Threshold queries, deletions over time |
| Rollback | history stack, no path compression | Undo the latest unions |
| Small-to-large member lists | a list of members per set | List every member; merge the smaller list into the larger for O(m + n log n) total ([cp-algorithms](https://cp-algorithms.com/data_structures/disjoint_set_union.html)) |

## A full run on eight elements

This table is the recorded state after each operation of the `DSU` class above. When two sets have equal size, the second root is hung under the first.

| Step | Operation | `parent` after | Sets |
| --- | --- | --- | --- |
| 0 | start | \[0, 1, 2, 3, 4, 5, 6, 7\] | 8 |
| 1 | union(0, 1) | \[0, 0, 2, 3, 4, 5, 6, 7\] | 7 |
| 2 | union(2, 3) | \[0, 0, 2, 2, 4, 5, 6, 7\] | 6 |
| 3 | union(4, 5) | \[0, 0, 2, 2, 4, 4, 6, 7\] | 5 |
| 4 | union(6, 7) | \[0, 0, 2, 2, 4, 4, 6, 6\] | 4 |
| 5 | union(1, 3) | \[0, 0, 0, 2, 4, 4, 6, 6\] | 3 |
| 6 | union(5, 7) | \[0, 0, 0, 2, 4, 4, 4, 6\] | 2 |
| 7 | union(3, 7) | \[0, 0, 0, 0, 0, 4, 4, 4\] | 1 |
| 8 | union(0, 7), returns false | \[0, 0, 0, 0, 0, 4, 4, 0\] | 1 |

Step 5: roots 0 and 2 each hold two elements, so the tie hangs 2 under 0. Step 7: `find(3)` climbs 3, 2, 0 and `find(7)` climbs 7, 6, 4; path compression rewires 3 and 7 on the way, then the two size-4 trees tie and 4 goes under 0. Step 8: 0 and 7 already share root 0, so `union` returns false and compression points 7 straight at 0.

After step 8 every node is within two hops of the root, which is what union by size guarantees (height at most log2 8 = 3).

## When to reach for a DSU, and when not to

Reach for a DSU when the problem only ever merges groups and asks about group membership.

| Signal in the problem | What the DSU gives you |
| --- | --- |
| Many "are x and y connected?" queries while edges are only added | `union` per edge, `connected` per query |
| Number or size of groups | `components` and `size[]` |
| "Does this edge create a cycle?" in an undirected graph | `union` returning false |
| Cheapest way to connect everything | Kruskal's algorithm |
| Things that are equal, similar or reachable transitively | each group is an equivalence class |
| Queries with a limit (time, weight, length) | sort edges and queries, then sweep |
| Edges removed over time | run time backwards and add edges |
| Two sides, opposite colours | parity DSU |
| Ratios or differences between items | weighted DSU |

Avoid it when you need an actual path or a shortest distance (use BFS or Dijkstra), when edges are removed between online queries, or when edges are directed and the direction matters. A DSU only models undirected connectivity.

## Pattern 1: connectivity, component counts and cycles

Treat every edge as `union(u, v)`. Afterwards `components` is the number of connected components and `connected(u, v)` says whether a path exists. `union` returns false exactly when u and v were already connected, so that edge closes a cycle.

Run on n = 4 with edges 0-1, 1-2, 2-3, 3-1:

| Edge | Result |
| --- | --- |
| 0-1 | joins two components |
| 1-2 | joins two components |
| 2-3 | joins two components |
| 3-1 | closes a cycle: both ends already sit under root 0 |

Two facts follow from the mechanics. Every successful `union` lowers the component count by exactly one. A graph on n vertices is a tree exactly when every `union` succeeds and there are n-1 edges.

## Pattern 2: Kruskal's minimum spanning tree

Sort the edges by weight and take an edge only when `union` succeeds. The DSU makes the cycle check near-constant, so the sort dominates and the total is O(m log m). [cp-algorithms](https://cp-algorithms.com/data_structures/disjoint_set_union.html) notes the DSU is what brings Kruskal from O(m log n + n²) down to O(m log n).

Run on 5 vertices with edges (0-1, w4), (0-2, w3), (1-2, w1), (1-3, w2), (2-3, w4), (3-4, w2). Ties keep their input order.

&#91;embedded content: Kruskal on a 5-vertex graph · 4 edges taken, 2 skipped\]

| Edge | Weight | Decision | Sets left | Total |
| --- | --- | --- | --- | --- |
| 1-2 | 1 | take | 4 | 1 |
| 1-3 | 2 | take | 3 | 3 |
| 3-4 | 2 | take | 2 | 5 |
| 0-2 | 3 | take | 1 | 8 |
| 0-1 | 4 | skip, closes a cycle | 1 | 8 |
| 2-3 | 4 | skip, closes a cycle | 1 | 8 |

```java
Arrays.sort(edges, (x, y) -> Integer.compare(x[2], y[2]));   // not x[2] - y[2], which can overflow
DSU d = new DSU(n);
int total = 0;
for (int[] e : edges)
    if (d.union(e[0], e[1])) total += e[2];
```

A spanning tree needs n-1 edges, so you can stop as soon as `d.components == 1`.

**Bottleneck paths.** If you add edges in increasing weight and stop the moment s and t become connected, the weight of the last edge added is the smallest possible value of the largest edge on any s-to-t path. That is the quantity behind "minimum effort" and "swim in rising water" style problems.

## Pattern 3: nodes that are not 0 to n-1

Real problems rarely hand you integer ids. These are the standard ways to fit them.

- **Grid cells.** Map (r, c) to `r * cols + c`. Union only with the right and down neighbours; the other two directions are covered when those neighbours take their turn.
- **A special "outside".** Add one dummy node (index n) and union every boundary element with it. Anything connected to the dummy touches the boundary.
- **Strings, emails, names.** Give each distinct key an int id with a `HashMap<String, Integer>`, or run the DSU on a `HashMap<String, String>` parent map.
- **Connect through a shared node, not pairwise.** If items share a property (a row, a column, a prime factor), union each item with a node that stands for the property instead of comparing every pair of items. That turns O(n²) pair checks into one union per item per property.
- **Aggregates at the root.** Keep size, min, max or sum in an array indexed by root, and merge it inside `union`.

```java
int id(int r, int c) { return r * cols + c; }

for (int r = 0; r < rows; r++)
    for (int c = 0; c < cols; c++) {
        // the condition depends on the problem; here: equal values
        if (r + 1 < rows && grid[r + 1][c] == grid[r][c]) d.union(id(r, c), id(r + 1, c));
        if (c + 1 < cols && grid[r][c + 1] == grid[r][c]) d.union(id(r, c), id(r, c + 1));
    }
```

An aggregate rides along with the union. Here, the smallest label in each set:

```java
int[] min;                                   // min[root] = smallest label in that set

boolean union(int a, int b) {
    int ra = find(a), rb = find(b);
    if (ra == rb) return false;
    if (size[ra] < size[rb]) { int t = ra; ra = rb; rb = t; }
    parent[rb] = ra;
    size[ra] += size[rb];
    min[ra] = Math.min(min[ra], min[rb]);    // merge the aggregate into the new root
    return true;
}
```

The root chosen by union by size is arbitrary. When a problem wants a specific leader (the smallest, say), keep it in an aggregate like `min[]` instead of reading it off `parent`. [cp-algorithms](https://cp-algorithms.com/data_structures/disjoint_set_union.html) makes the same point.

## Variant: parity DSU (bipartite check, online)

Store each node's colour relative to its parent: `parity[x] = colour(x) xor colour(parent[x])`. `find` accumulates parity along the path, so path compression stays valid. For an edge a-b with the same root, equal colours mean an odd cycle and the graph is not bipartite. With different roots, hang one root under the other with `parity[rb] = parity[a] ^ parity[b] ^ 1`, so a and b land on opposite sides. [cp-algorithms](https://cp-algorithms.com/data_structures/disjoint_set_union.html) derives the same formula.

&#91;embedded content: parity colouring · a 4-cycle and a triangle\]

```java
class ParityDSU {
    int[] parent, size, parity;

    ParityDSU(int n) {
        parent = new int[n]; size = new int[n]; parity = new int[n];
        for (int i = 0; i < n; i++) { parent[i] = i; size[i] = 1; }
    }

    int find(int x) {
        if (parent[x] == x) return x;
        int p = parent[x];
        int r = find(p);
        parity[x] ^= parity[p];          // parity[p] is now relative to the root
        parent[x] = r;
        return r;
    }

    boolean addEdge(int a, int b) {      // false if the edge creates an odd cycle
        int ra = find(a), rb = find(b);
        if (ra == rb) return parity[a] != parity[b];
        if (size[ra] < size[rb]) { int t = ra; ra = rb; rb = t; }
        parent[rb] = ra;
        parity[rb] = parity[a] ^ parity[b] ^ 1;
        size[ra] += size[rb];
        return true;
    }
}
```

Recorded runs. A 4-cycle is bipartite:

| Edge | Accepted | `parent` | `parity` |
| --- | --- | --- | --- |
| 0-1 | yes | \[0, 0, 2, 3\] | \[0, 1, 0, 0\] |
| 1-2 | yes | \[0, 0, 0, 3\] | \[0, 1, 0, 0\] |
| 2-3 | yes | \[0, 0, 0, 0\] | \[0, 1, 0, 1\] |
| 3-0 | yes: same root, parities 1 and 0 differ | \[0, 0, 0, 0\] | \[0, 1, 0, 1\] |

A triangle is not:

| Edge | Accepted | `parent` | `parity` |
| --- | --- | --- | --- |
| 0-1 | yes | \[0, 0, 2\] | \[0, 1, 0\] |
| 1-2 | yes | \[0, 0, 0\] | \[0, 1, 0\] |
| 2-0 | no: same root, both parity 0 | \[0, 0, 0\] | \[0, 1, 0\] |

This class matched a BFS two-colouring on 3,000 random graphs. For a static graph a BFS colouring is simpler; the DSU wins when edges arrive online or when the constraints say "these two must differ".

## Variant: weighted DSU (relative values)

Store the offset to the parent: `pot[x] = val[x] - val[parent[x]]`. `find` adds up offsets along the path while compressing, so after `find(x)` the entry `pot[x]` is x's value relative to its root. A fact "val\[a\] - val\[b\] = d" either merges two roots, setting `pot[ra] = d - pot[a] + pot[b]`, or, when the roots already match, is checked against `pot[a] - pot[b]`. For ratios the same code works with multiplication in place of addition and division in place of subtraction.

```java
class WeightedDSU {
    int[] parent; long[] pot;                // pot[x] = val[x] - val[parent[x]]

    WeightedDSU(int n) {
        parent = new int[n]; pot = new long[n];
        for (int i = 0; i < n; i++) parent[i] = i;
    }

    int find(int x) {
        if (parent[x] == x) return x;
        int p = parent[x];
        int r = find(p);
        pot[x] += pot[p];                    // pot[p] is now relative to the root
        parent[x] = r;
        return r;
    }

    boolean addFact(int a, int b, long d) {  // val[a] - val[b] = d; false on a contradiction
        int ra = find(a), rb = find(b);
        if (ra == rb) return pot[a] - pot[b] == d;
        parent[ra] = rb;
        pot[ra] = d - pot[a] + pot[b];
        return true;
    }

    Long diff(int a, int b) {                // val[a] - val[b], or null if unknown
        if (find(a) != find(b)) return null;
        return pot[a] - pot[b];
    }
}
```

This version links without a size rule so the algebra stays visible. To add union by size, hang the other root instead and negate the offset: `pot[rb] = -(d - pot[a] + pot[b])`.

Recorded run with a = 0, b = 1, c = 2:

| Step | Call | `parent` | `pot` | Result |
| --- | --- | --- | --- | --- |
| 1 | addFact(0, 1, 3): a - b = 3 | \[1, 1, 2\] | \[3, 0, 0\] | true |
| 2 | addFact(1, 2, 2): b - c = 2 | \[1, 2, 2\] | \[3, 2, 0\] | true |
| 3 | diff(0, 2) | \[2, 2, 2\] | \[5, 2, 0\] | 5 |
| 4 | addFact(0, 2, 4) | unchanged | unchanged | false, contradicts 5 |
| 5 | addFact(0, 2, 5) | unchanged | unchanged | true, consistent |

In step 3, `find(0)` climbs 0, 1, 2 and compresses, so `pot[0]` becomes 3 + 2 = 5.

## Variant: offline processing and reverse time

A DSU only merges and never splits, and two tricks make that enough.

**Sort by a limit.** For queries like "is there a path using only edges lighter than L?", sort the edges by weight and the queries by L. Sweep through the queries, and before answering each one, union every edge below its limit. Keep each query's original index so the answers can be put back in order. The same sweep answers "earliest time when X holds": sort edges by time and stop when the condition becomes true.

**Reverse time for deletions.** If edges disappear over time, run the clock backwards. Start from the graph after all deletions, then add the edges back in reverse order of deletion. The state after t deletions is the state after adding back k - t edges, where k is the total number of deletions.

Example: a 5-cycle with edges e0 = 0-1, e1 = 1-2, e2 = 2-3, e3 = 3-4, e4 = 4-0. Delete e1, then e3, then e0, and count components after each deletion.

| Deletions done | Components | How the backwards run gets it |
| --- | --- | --- |
| 3 (e1, e3, e0 gone) | 3 | Build with e2 and e4 only |
| 2 | 2 | Add back e0 |
| 1 | 1 | Add back e3 |
| 0 | 1 | Add back e1 |

Read forwards, the cycle stays connected after e1 goes, splits in two after e3, and in three after e0. The recorded run printed `[1, 1, 2, 3]` for 0 to 3 deletions and matched a brute-force rebuild after every deletion.

## Variant: rollback DSU

To undo a union you cannot have compressed any paths, so a rollback DSU uses union by size only. `find` costs O(log n), and every union call pushes a record on a stack. Undoing pops the record, makes the child root its own root again and subtracts its size from the parent. It supports offline dynamic connectivity (edges that exist only during a time interval). It is rare on LeetCode and common in contests.

```java
class RollbackDSU {
    int[] parent, size;
    Deque<int[]> history = new ArrayDeque<>();

    RollbackDSU(int n) {
        parent = new int[n]; size = new int[n];
        for (int i = 0; i < n; i++) { parent[i] = i; size[i] = 1; }
    }

    int find(int x) { while (parent[x] != x) x = parent[x]; return x; }   // no compression

    boolean union(int a, int b) {
        int ra = find(a), rb = find(b);
        if (ra == rb) { history.push(new int[]{-1, -1}); return false; }  // one record per call
        if (size[ra] < size[rb]) { int t = ra; ra = rb; rb = t; }
        parent[rb] = ra;
        size[ra] += size[rb];
        history.push(new int[]{rb, ra});
        return true;
    }

    void rollback() {                        // undo the latest union() call
        int[] h = history.pop();
        if (h[0] == -1) return;
        parent[h[0]] = h[0];
        size[h[1]] -= size[h[0]];
    }
}
```

Recorded run on n = 5:

| Step | `parent` | `size` |
| --- | --- | --- |
| union(0, 1) | \[0, 0, 2, 3, 4\] | \[2, 1, 1, 1, 1\] |
| union(2, 3) | \[0, 0, 2, 2, 4\] | \[2, 1, 2, 1, 1\] |
| union(1, 3): root 2 goes under root 0 | \[0, 0, 0, 2, 4\] | \[4, 1, 2, 1, 1\] |
| rollback | \[0, 0, 2, 2, 4\] | \[2, 1, 2, 1, 1\] |
| rollback | \[0, 0, 2, 3, 4\] | \[2, 1, 1, 1, 1\] |

`size` is only meaningful at roots, so stale values at non-roots are harmless.

## Pitfalls in Java

- **Recursion depth.** A recursive `find` is safe with union by size (depth at most log2 n). With compression alone, a chain of 100,000 nodes can throw `StackOverflowError`. The iterative form below uses path halving and needs no recursion.
- **Compare roots, never parents.** `parent[a] == parent[b]` is wrong unless both are already compressed. Use `find(a) == find(b)`.
- **`size[]` is only valid at roots.** Call `find` first, then read `size[root]`.
- **Group by `find(i)`, not `parent[i]`.** After unions, a non-root's parent can be two or more hops from its root.
- **1-indexed inputs.** Allocate `n + 1` and ignore index 0, or subtract 1 on the way in.
- **Directed edges.** A DSU treats every edge as undirected. Directed problems need extra reasoning, such as in-degrees.
- **A fresh DSU per test.** A judge may reuse one `Solution` object across test cases. Create the DSU inside the method instead of keeping it in a field from an earlier call.
- **Offline queries.** Keep each query's original index when you sort, or the answers come back in the wrong order.
- **Comparators.** Sort with `Integer.compare(x, y)`; `x - y` can overflow.

```java
int find(int x) {
    while (parent[x] != x) {
        parent[x] = parent[parent[x]];   // path halving
        x = parent[x];
    }
    return x;
}
```

## Complexity cheat sheet

| Structure | `find` | `union` | Extra memory |
| --- | --- | --- | --- |
| Naive | O(n) | O(n) | none beyond `parent[]` |
| Union by size or rank only | O(log n) | O(log n) | `size[]` or `rank[]` |
| Path compression only | O(log n) amortised | O(log n) amortised | none |
| Compression + size or rank | O(α(n)) amortised | O(α(n)) amortised | `size[]` or `rank[]` |
| Rollback (size only) | O(log n) | O(log n) | history stack |
| Parity or weighted | same as the DSU underneath | same | one more array |

Building any of these is O(n). Kruskal costs O(m log m) for the sort plus m unions at O(α(n)) each.

## Practice problems by pattern (no solutions)

Attempt each problem after rereading the section named in the Pattern column; that column names an idea to revisit and nothing more. Tiers are my own order of difficulty, not LeetCode's labels, and the pattern tags are my own classification. "P" marks a problem that, as far as I know, needs LeetCode Premium. Numbers and titles come from the [walkccc Union-Find list](https://walkccc.me/LeetCode/topics/data-structures/graph/union-find); search LeetCode by number.

**Tier 1: plain connectivity, counts and cycles**

| # | Problem | Pattern |
| --- | --- | --- |
| 1971 | Find if Path Exists in Graph | connectivity |
| 547 | Number of Provinces | component count |
| 323 (P) | Number of Connected Components in an Undirected Graph | component count |
| 684 | Redundant Connection | cycle detection |
| 261 (P) | Graph Valid Tree | cycle detection + component count |
| 1319 | Number of Operations to Make Network Connected | component count |
| 990 | Satisfiability of Equality Equations | equivalence classes |
| 1061 | Lexicographically Smallest Equivalent String | equivalence classes + aggregate at the root |
| 2316 | Count Unreachable Pairs of Nodes in an Undirected Graph | component sizes |
| 2685 | Count the Number of Complete Components | component sizes |

**Tier 2: grids, strings and other kinds of nodes**

| # | Problem | Pattern |
| --- | --- | --- |
| 200 | Number of Islands | grid cells as nodes |
| 695 | Max Area of Island | grid cells + size |
| 130 | Surrounded Regions | dummy node |
| 1905 | Count Sub Islands | grid cells as nodes |
| 827 | Making A Large Island | grid cells + size |
| 959 | Regions Cut By Slashes | grid with extra nodes |
| 721 | Accounts Merge | non-integer nodes |
| 839 | Similar String Groups | non-integer nodes |
| 947 | Most Stones Removed with Same Row or Column | shared node |
| 1202 | Smallest String With Swaps | components + per-component work |
| 1722 | Minimize Hamming Distance After Swap Operations | components + per-component work |
| 2948 | Make Lexicographically Smallest Array by Swapping Elements | components after sorting |
| 128 | Longest Consecutive Sequence | aggregate at the root (other approaches exist) |
| 952 | Largest Component Size by Common Factor | shared node |
| 1998 | GCD Sort of an Array | shared node |
| 2709 | Greatest Common Divisor Traversal | shared node |

**Tier 3: spanning trees and bottleneck paths**

| # | Problem | Pattern |
| --- | --- | --- |
| 1584 | Min Cost to Connect All Points | Kruskal |
| 1135 (P) | Connecting Cities With Minimum Cost | Kruskal |
| 1168 (P) | Optimize Water Distribution in a Village | Kruskal + dummy node |
| 1579 | Remove Max Number of Edges to Keep Graph Fully Traversable | more than one DSU |
| 1489 | Find Critical and Pseudo-Critical Edges in Minimum Spanning Tree | Kruskal variations |
| 1631 | Path With Minimum Effort | bottleneck path (redo your Dijkstra solution with a DSU) |
| 778 | Swim in Rising Water | bottleneck path |
| 1102 (P) | Path With Maximum Minimum Value | bottleneck path |
| 2492 | Minimum Score of a Path Between Two Cities | component aggregate |
| 3108 | Minimum Cost Walk in Weighted Graph | component aggregate |

**Tier 4: offline queries and reverse time**

| # | Problem | Pattern |
| --- | --- | --- |
| 1697 | Checking Existence of Edge Length Limited Paths | sort edges and queries |
| 1101 (P) | The Earliest Moment When Everyone Become Friends | sort edges by time |
| 2092 | Find All People With Secret | time-ordered merging |
| 1627 | Graph Connectivity With Threshold | implicit edges |
| 2421 | Number of Good Paths | sort by value + aggregate |
| 1970 | Last Day Where You Can Still Cross | reverse time |
| 803 | Bricks Falling When Hit | reverse time + dummy node |
| 2382 | Maximum Segment Sum After Removals | reverse time + aggregate |
| 305 (P) | Number of Islands II | edges added online |

**Tier 5: parity, weights and harder modelling**

| # | Problem | Pattern |
| --- | --- | --- |
| 785 | Is Graph Bipartite? | parity |
| 886 | Possible Bipartition | parity |
| 2493 | Divide Nodes Into the Maximum Number of Groups | bipartite check + components |
| 399 | Evaluate Division | weighted |
| 765 | Couples Holding Hands | components |
| 1632 | Rank Transform of a Matrix | components processed by value |
| 924 | Minimize Malware Spread | component sizes |
| 928 | Minimize Malware Spread II | harder variant of 924 |
| 1361 | Validate Binary Tree Nodes | tree conditions |
| 685 | Redundant Connection II | directed graph |
| 2157 | Groups of Strings | nodes built from bitmasks |

**Beyond LeetCode.** The [cp-algorithms DSU article](https://cp-algorithms.com/data_structures/disjoint_set_union.html) lists Codeforces 25D (Roads not only in Berland), Timus 1003 (Parity) and SPOJ CHAIN (Strange Food Chain); the last two are good parity and relation exercises.

**Suggested order.** Finish Tier 1 first, then Tier 2. After that, take one problem from each remaining tier before going deep on any. Return to a solved problem and redo it with a different variant from this guide; that is where the patterns stick.

## Sources

- [Disjoint Set Union, cp-algorithms](https://cp-algorithms.com/data_structures/disjoint_set_union.html): definition, optimisations, complexity, parity, applications.
- [Union Find templates, lctemplates](https://lctemplates.readthedocs.io/en/latest/union-find.html): size and rank templates, weighted DSU.
- [Union-Find problem list, walkccc](https://walkccc.me/LeetCode/topics/data-structures/graph/union-find): problem numbers and titles.
- [10 Interesting Problems of DSU, LeetCode Discuss](https://leetcode.com/discuss/post/7336923/10-interesting-problems-of-dsudisjoint-s-x147/): problem patterns.

All code and traces were compiled and run on Java 21 and cross-checked against BFS on random graphs. The path halving snippet and the problem pattern tags come from general knowledge and my own classification, not from the pages above.
