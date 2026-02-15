import random
rows = 20
cols = 20
# up, right, down, bottom-right, left, top-left
directions = [
    (-1, 0),
    (0, 1),
    (1, 0),
    (1, 1),
    (0, -1),
    (-1, -1),
]
obstacle_prob = 0.03

def make_grid():
    grid = []
    for r in range(rows):
        row = []
        for c in range(cols):
            row.append(0)
        grid.append(row)
    return grid

def place_walls(grid, count=40):
    placed = 0
    while placed < count:
        r = random.randint(0, rows-1)
        c = random.randint(0, cols-1)
        if grid[r][c] == 0:
            grid[r][c] = 1
            placed += 1

def get_neighbors(grid, pos):
    nbrs = []
    for dr, dc in directions:
        nr = pos[0] + dr
        nc = pos[1] + dc
        if 0 <= nr < rows and 0 <= nc < cols:
            if grid[nr][nc] != 1:
                nbrs.append((nr, nc))
    return nbrs

def spawn_obstacle(grid, start, target):
    if random.random() < obstacle_prob:
        r = random.randint(0, rows-1)
        c = random.randint(0, cols-1)
        if grid[r][c] == 0 and (r,c) != start and (r,c) != target:
            grid[r][c] = 1
            return (r,c)
    return None

def get_path(came_from, start, target):
    path = []
    cur = target
    while cur != start:
        path.append(cur)
        if cur not in came_from:
            return []
        cur = came_from[cur]
    path.append(start)
    path.reverse()
    return path