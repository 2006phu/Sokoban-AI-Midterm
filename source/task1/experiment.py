# experiment.py
# Thanh vien B (Huy) phu trach - Req 3
# So sanh hieu suat UCS vs A*
# Da sua loi: dung ky tu tuong '%' thay '#', bo Manhattan, dung BFS + permutation

import heapq
import time
import itertools
from collections import deque
import os

# ============================================================
# HAM DOC BAN DO VA XU LY TRANG THAI (dung chung)
# ============================================================

def load_map(filepath):
    """Doc ban do tu file text. Ky tu tuong la '%' theo de bai."""
    walls = set()
    boxes = set()
    goals = set()
    agent = None

    with open(filepath, 'r') as f:
        for r, line in enumerate(f):
            for c, char in enumerate(line.strip('\n')):
                pos = (r, c)
                if char == '%':
                    walls.add(pos)
                elif char == 'B':
                    boxes.add(pos)
                elif char == 'C':
                    goals.add(pos)
                    boxes.add(pos)
                elif char == 'D':
                    goals.add(pos)
                elif char == 'A':
                    agent = pos

    initial_state = (agent, frozenset(boxes))
    return initial_state, walls, goals


def is_goal(state, goals):
    """Kiem tra tat ca goals deu co box."""
    _, boxes = state
    return goals.issubset(boxes)


def get_successors(state, walls):
    """Sinh cac trang thai ke tu trang thai hien tai."""
    successors = []
    agent_pos, boxes = state
    r, c = agent_pos

    for d_r, d_c in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        new_r, new_c = r + d_r, c + d_c
        new_agent_pos = (new_r, new_c)

        if new_agent_pos in walls:
            continue

        if new_agent_pos in boxes:
            new_box_pos = (new_r + d_r, new_c + d_c)
            if new_box_pos in boxes or new_box_pos in walls:
                continue
            new_boxes = (boxes - {new_agent_pos}) | {new_box_pos}
            successors.append((new_agent_pos, frozenset(new_boxes)))
        else:
            successors.append((new_agent_pos, boxes))

    return successors


# ============================================================
# HAM HEURISTIC (BFS distance + Permutation)
# Khong dung Manhattan/Euclidean theo yeu cau de bai
# ============================================================

def bfs_distance(start, goals, walls):
    """
    Tim khoang cach ngan nhat (BFS) tu start den moi goal.
    Tra ve dict {goal_pos: distance}.
    """
    queue = deque([(start, 0)])
    explored = {start}
    distance = {}

    while queue:
        curr, dist = queue.popleft()
        if curr in goals:
            distance[curr] = dist
            if len(distance) == len(goals):
                break
        r, c = curr
        for d_r, d_c in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            next_pos = (r + d_r, c + d_c)
            if next_pos not in walls and next_pos not in explored:
                explored.add(next_pos)
                queue.append((next_pos, dist + 1))

    for g in goals:
        if g not in distance:
            distance[g] = float('inf')
    return distance


def heuristic_bfs(state, goals, walls):
    """
    Heuristic dung BFS distance + permutation (ghep noi toi uu).
    Thay the Manhattan distance bi cam trong de bai.
    """
    _, boxes = state
    unmatched_boxes = [b for b in boxes if b not in goals]
    unmatched_goals = [g for g in goals if g not in boxes]

    if not unmatched_boxes:
        return 0

    n = len(unmatched_boxes)
    # Xay dung ma tran chi phi BFS
    cost_matrix = []
    for b in unmatched_boxes:
        dist_dict = bfs_distance(b, set(unmatched_goals), walls)
        row = [dist_dict.get(g, float('inf')) for g in unmatched_goals]
        cost_matrix.append(row)

    # Tim ghep noi toi uu bang permutation
    # (Voi so box nho <= 7, permutation chap nhan duoc)
    min_cost = float('inf')
    for perm in itertools.permutations(range(n)):
        total = sum(cost_matrix[i][perm[i]] for i in range(n))
        if total < min_cost:
            min_cost = total

    return min_cost


# ============================================================
# THUAT TOAN TIM KIEM
# ============================================================

def ucs_search(initial_state, walls, goals):
    """Uniform Cost Search - Req 2."""
    start_time = time.time()
    counter = itertools.count()

    frontier = []
    heapq.heappush(frontier, (0, next(counter), initial_state))

    explored = set()
    nodes_expanded = 0
    max_frontier = 0

    while frontier:
        max_frontier = max(max_frontier, len(frontier))
        g_cost, _, current_state = heapq.heappop(frontier)

        if current_state in explored:
            continue

        explored.add(current_state)
        nodes_expanded += 1

        if is_goal(current_state, goals):
            return {
                "time": time.time() - start_time,
                "nodes": nodes_expanded,
                "max_frontier": max_frontier,
                "cost": g_cost
            }

        for next_state in get_successors(current_state, walls):
            if next_state not in explored:
                heapq.heappush(frontier, (g_cost + 1, next(counter), next_state))

    return None


def a_star_search(initial_state, walls, goals):
    """A* Search voi heuristic BFS + permutation - Req 2."""
    start_time = time.time()
    counter = itertools.count()

    h_init = heuristic_bfs(initial_state, goals, walls)
    frontier = []
    heapq.heappush(frontier, (h_init, 0, next(counter), initial_state))

    explored = set()
    nodes_expanded = 0
    max_frontier = 0

    while frontier:
        max_frontier = max(max_frontier, len(frontier))
        f_cost, g_cost, _, current_state = heapq.heappop(frontier)

        if current_state in explored:
            continue

        explored.add(current_state)
        nodes_expanded += 1

        if is_goal(current_state, goals):
            return {
                "time": time.time() - start_time,
                "nodes": nodes_expanded,
                "max_frontier": max_frontier,
                "cost": g_cost
            }

        for next_state in get_successors(current_state, walls):
            if next_state not in explored:
                new_g = g_cost + 1
                h = heuristic_bfs(next_state, goals, walls)
                heapq.heappush(frontier, (new_g + h, new_g, next(counter), next_state))

    return None


# ============================================================
# CHAY THI NGHIEM (Req 3)
# ============================================================

if __name__ == "__main__":
    maps = [
        ("Easy",   "maps/ez_map.txt"),
        ("Medium", "maps/med_map.txt"),
        ("Hard",   "maps/hard_map.txt"),
        ("Sample", "maps/example_map.txt"),
    ]

    header = f"{'Ban do':<10} | {'Thuat toan':<12} | {'Thoi gian (s)':<15} | {'Node expanded':<15} | {'Max Frontier':<15} | {'Cost':<8}"
    print(header)
    print("-" * len(header))

    for map_name, filepath in maps:
        if not os.path.exists(filepath):
            print(f"{map_name:<10} | LỖI: Khong tim thay file '{filepath}'")
            continue

        initial_state, walls, goals = load_map(filepath)

        # Chay UCS
        res_ucs = ucs_search(initial_state, walls, goals)
        if res_ucs:
            print(f"{map_name:<10} | {'UCS':<12} | {res_ucs['time']:<15.4f} | {res_ucs['nodes']:<15} | {res_ucs['max_frontier']:<15} | {res_ucs['cost']:<8}")
        else:
            print(f"{map_name:<10} | {'UCS':<12} | Khong tim duoc loi giai")

        # Chay A*
        res_astar = a_star_search(initial_state, walls, goals)
        if res_astar:
            print(f"{'':<10} | {'A*':<12} | {res_astar['time']:<15.4f} | {res_astar['nodes']:<15} | {res_astar['max_frontier']:<15} | {res_astar['cost']:<8}")
        else:
            print(f"{'':<10} | {'A*':<12} | Khong tim duoc loi giai")

        # Kiem tra cost bang nhau
        if res_ucs and res_astar:
            match = "PASS" if res_ucs['cost'] == res_astar['cost'] else "FAIL"
            print(f"{'':<10} | {'CHECK':<12} | Cost UCS == A*: {match}")

        print("-" * len(header))
