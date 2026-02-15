from collections import deque
import heapq
from grid_utils import get_neighbors, spawn_obstacle, get_path

# bfs search
def bfs(grid, start, target):
    q = deque()
    q.append(start)
    visited = set()
    visited.add(start)
    parent = {}
    fset = {start}
    while q:
        cur = q.popleft()
        fset.discard(cur)
        if cur == target:
            path = get_path(parent, start, target)
            yield list(fset), visited, path
            return
        for nb in get_neighbors(grid, cur):
            if nb not in visited:
                visited.add(nb)
                parent[nb] = cur
                q.append(nb)
                fset.add(nb)
        spawn_obstacle(grid, start, target)
        # removee blocked nodes
        bad = []
        for node in list(q):
            r,c = node
            if grid[r][c] != 0:
                bad.append(node)
        for node in bad:
            q.remove(node)
            fset.discard(node)
        yield list(fset), visited.copy(), None
    yield [], visited.copy(), []

# dfs serach
def dfs(grid, start, target):
    stack = [start]
    visited = set()
    parent = {}
    fset = {start}
    while stack:
        cur = stack.pop()
        fset.discard(cur)
        if cur in visited:
            continue
        visited.add(cur)
        if cur == target:
            path = get_path(parent, start, target)
            yield list(fset), visited, path
            return
        nbrs = get_neighbors(grid, cur)
        for nb in reversed(nbrs):
            if nb not in visited:
                parent[nb] = cur
                stack.append(nb)
                fset.add(nb)
        spawn_obstacle(grid, start, target)
        new_stack = []
        for node in stack:
            r,c = node
            if grid[r][c] == 0 or node == start or node == target:
                new_stack.append(node)
            else:
                fset.discard(node)
        stack = new_stack
        yield list(fset), visited.copy(), None
    yield [], visited.copy(), []

# uniform cost serch
def ucs(grid, start, target):
    cnt = 0
    heap = []
    heapq.heappush(heap, (0, cnt, start))
    cnt += 1
    visited = set()
    parent = {}
    costs = {start: 0}
    fset = {start}
    while heap:
        cost, _, cur = heapq.heappop(heap)
        fset.discard(cur)
        if cur in visited:
            continue
        visited.add(cur)
        if cur == target:
            path = get_path(parent, start, target)
            yield list(fset), visited, path
            return
        for nb in get_neighbors(grid, cur):
            dr = abs(nb[0]-cur[0])
            dc = abs(nb[1]-cur[1])
            if dr==1 and dc==1:
                sc = 1.4  # diagnol cost
            else:
                sc = 1.0
            nc = cost + sc
            if nb not in costs or nc < costs[nb]:
                costs[nb] = nc
                parent[nb] = cur
                heapq.heappush(heap, (nc, cnt, nb))
                cnt += 1
                fset.add(nb)
        spawn_obstacle(grid, start, target)
        new_heap = []
        for item in heap:
            r,c = item[2]
            if grid[r][c] == 0 or item[2]==start or item[2]==target:
                new_heap.append(item)
            else:
                fset.discard(item[2])
        heapq.heapify(new_heap)
        heap = new_heap
        yield list(fset), visited.copy(), None
    yield [], visited.copy(), []

# depth limted search
def dls(grid, start, target, limit=20):
    visited = set()
    parent = {}
    fset = set()
    stack = [(start, 0)]
    fset.add(start)
    while stack:
        cur, depth = stack.pop()
        fset.discard(cur)
        if cur in visited:
            continue
        visited.add(cur)
        if cur == target:
            path = get_path(parent, start, target)
            yield list(fset), visited, path
            return
        if depth < limit:
            for nb in reversed(get_neighbors(grid, cur)):
                if nb not in visited:
                    parent[nb] = cur
                    stack.append((nb, depth+1))
                    fset.add(nb)
        spawn_obstacle(grid, start, target)
        new_stack = []
        for node, d in stack:
            r,c = node
            if grid[r][c]==0 or node==start or node==target:
                new_stack.append((node,d))
            else:
                fset.discard(node)
        stack = new_stack
        yield list(fset), visited.copy(), None
    yield [], visited.copy(), []

# iteratvie deepning dfs
def iddfs(grid, start, target, max_depth=30):
    all_visited = set()
    for dep_limit in range(max_depth+1):
        visited = set()
        parent = {}
        stack = [(start, 0)]
        fset = set()
        fset.add(start)
        while stack:
            cur, depth = stack.pop()
            fset.discard(cur)
            if cur in visited:
                continue
            visited.add(cur)
            all_visited.add(cur)
            if cur == target:
                path = get_path(parent, start, target)
                yield list(fset), all_visited, path
                return
            if depth < dep_limit:
                for nb in reversed(get_neighbors(grid, cur)):
                    if nb not in visited:
                        parent[nb] = cur
                        stack.append((nb, depth+1))
                        fset.add(nb)
            spawn_obstacle(grid, start, target)
            new_stack = []
            for node, d in stack:
                r,c = node
                if grid[r][c]==0 or node==start or node==target:
                    new_stack.append((node,d))
                else:
                    fset.discard(node)
            stack = new_stack
            yield list(fset), all_visited.copy(), None
    yield [], all_visited.copy(), []

# bidirecional search
def bidirectional(grid, start, target):
    q_s = deque([start])
    q_t = deque([target])
    vis_s = {start}
    vis_t = {target}
    par_s = {}
    par_t = {}
    fset = {start, target}
    while q_s or q_t:
        if q_s:
            cur_s = q_s.popleft()
            fset.discard(cur_s)
            if cur_s in vis_t:
                path = build_bidir_path(par_s, par_t, start, target, cur_s)
                allvis = vis_s | vis_t
                yield list(fset), allvis, path
                return
            for nb in get_neighbors(grid, cur_s):
                if nb not in vis_s:
                    vis_s.add(nb)
                    par_s[nb] = cur_s
                    q_s.append(nb)
                    fset.add(nb)
        if q_t:
            cur_t = q_t.popleft()
            fset.discard(cur_t)
            if cur_t in vis_s:
                path = build_bidir_path(par_s, par_t, start, target, cur_t)
                allvis = vis_s | vis_t
                yield list(fset), allvis, path
                return
            for nb in get_neighbors(grid, cur_t):
                if nb not in vis_t:
                    vis_t.add(nb)
                    par_t[nb] = cur_t
                    q_t.append(nb)
                    fset.add(nb)
        spawn_obstacle(grid, start, target)
        # removve blocked ones
        for q in [q_s, q_t]:
            bad = []
            for node in list(q):
                r,c = node
                if grid[r][c] != 0 and node != start and node != target:
                    bad.append(node)
            for node in bad:
                q.remove(node)
                fset.discard(node)
        allvis = vis_s | vis_t
        yield list(fset), allvis.copy(), None
    allvis = vis_s | vis_t
    yield [], allvis.copy(), []

def build_bidir_path(par_s, par_t, start, target, meet):
    # build from start to meet then meet to target
    p1 = []
    cur = meet
    while cur != start:
        p1.append(cur)
        if cur not in par_s:
            return []
        cur = par_s[cur]
    p1.append(start)
    p1.reverse()
    p2 = []
    cur = meet
    while cur != target:
        if cur not in par_t:
            return []
        cur = par_t[cur]
        p2.append(cur)
    return p1 + p2
