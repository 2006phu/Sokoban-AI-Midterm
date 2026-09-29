# heuristic_verification.py
# Thanh vien B (Huy) phu trach - Req 4
# Kiem chung tinh admissible va consistent cua heuristic
# Da sua: dung ky tu tuong '%', sua typo ten thu muc, dung BFS distance

import heapq
import itertools
from collections import deque

# ============================================================
# HAM DOC BAN DO VA XU LY TRANG THAI
# ============================================================

def load_map(filepath):
    """Doc ban do tu file. Ky tu tuong: '%'."""
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
    _, boxes = state
    return goals.issubset(boxes)


def get_successors(state, walls):
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
# HAM HEURISTIC (BFS + Permutation)
# ============================================================

def bfs_distance(start, goals, walls):
    """BFS tim khoang cach ngan nhat tu start den moi goal."""
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


def heuristic_func(state, goals, walls):
    """Heuristic BFS distance + permutation ghep noi toi uu."""
    _, boxes = state
    unmatched_boxes = [b for b in boxes if b not in goals]
    unmatched_goals = [g for g in goals if g not in boxes]

    if not unmatched_boxes:
        return 0

    n = len(unmatched_boxes)
    cost_matrix = []
    for b in unmatched_boxes:
        dist_dict = bfs_distance(b, set(unmatched_goals), walls)
        row = [dist_dict.get(g, float('inf')) for g in unmatched_goals]
        cost_matrix.append(row)

    min_cost = float('inf')
    for perm in itertools.permutations(range(n)):
        total = sum(cost_matrix[i][perm[i]] for i in range(n))
        if total < min_cost:
            min_cost = total

    return min_cost


# ============================================================
# TINH CHI PHI THUC (h*) BANG UCS
# ============================================================

def get_true_cost(start_state, walls, goals):
    """Chay UCS tu start_state de tim chi phi toi uu thuc su h*(n)."""
    counter = itertools.count()
    frontier = []
    heapq.heappush(frontier, (0, next(counter), start_state))
    explored = set()

    while frontier:
        g_cost, _, current_state = heapq.heappop(frontier)
        if current_state in explored:
            continue
        explored.add(current_state)

        if is_goal(current_state, goals):
            return g_cost

        for next_state in get_successors(current_state, walls):
            if next_state not in explored:
                heapq.heappush(frontier, (g_cost + 1, next(counter), next_state))

    return float('inf')


# ============================================================
# THU THAP TRANG THAI MAU BANG BFS
# ============================================================

def generate_sample_states(initial_state, walls, max_states=1500):
    """
    Dung BFS loang tu trang thai dau,
    thu thap toi da max_states trang thai lam du lieu test.
    """
    states = []
    queue = deque([initial_state])
    explored = {initial_state}

    while queue and len(states) < max_states:
        current = queue.popleft()
        states.append(current)

        for nxt in get_successors(current, walls):
            if nxt not in explored:
                explored.add(nxt)
                queue.append(nxt)

    return states


# ============================================================
# KIEM CHUNG (Req 4)
# ============================================================

def verify_heuristic(filepath):
    """Kiem chung admissible va consistent tren ban do."""
    initial_state, walls, goals = load_map(filepath)
    print(f"Dang trich xuat du lieu tu {filepath}...")
    test_states = generate_sample_states(initial_state, walls, 1500)
    print(f"Da thu thap {len(test_states)} trang thai mau.\n")

    # --- KIEM CHUNG CONSISTENT ---
    # h(n) <= c(n, n') + h(n')  voi c = 1
    # Tuong duong: h(n) - h(n') <= 1
    consistent_violations = 0
    pair_count = 0

    for state in test_states:
        h_n = heuristic_func(state, goals, walls)
        for nxt_state in get_successors(state, walls):
            h_nxt = heuristic_func(nxt_state, goals, walls)
            pair_count += 1
            if h_n - h_nxt > 1:
                consistent_violations += 1

    print("=== KIEM CHUNG CONSISTENT ===")
    print(f"Tong so cap kiem tra: {pair_count}")
    print(f"So vi pham: {consistent_violations}")
    if consistent_violations == 0:
        print("Ket luan: CONSISTENT ✅")
    else:
        print("Ket luan: KHONG CONSISTENT ❌")

    # --- KIEM CHUNG ADMISSIBLE ---
    # h(n) <= h*(n) cho moi state
    # Chi kiem tra 50 state dau (vi tinh h* bang UCS rat cham)
    admissible_violations = 0
    state_count = 0
    num_check = min(50, len(test_states))

    print(f"\n=== KIEM CHUNG ADMISSIBLE ===")
    print(f"Dang chay UCS cho {num_check} trang thai (co the mat vai phut)...")

    for state in test_states[:num_check]:
        h_n = heuristic_func(state, goals, walls)
        h_star_n = get_true_cost(state, walls, goals)

        if h_star_n != float('inf'):
            state_count += 1
            if h_n > h_star_n:
                admissible_violations += 1
                print(f"  VI PHAM: h(n)={h_n} > h*(n)={h_star_n}")

    print(f"Tong so state kiem tra: {state_count}")
    print(f"So vi pham: {admissible_violations}")
    if admissible_violations == 0:
        print("Ket luan: ADMISSIBLE ✅")
    else:
        print("Ket luan: KHONG ADMISSIBLE ❌")


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    import os

    print("=" * 60)
    print("KIEM CHUNG HEURISTIC - Req 4")
    print("Heuristic: BFS distance + Permutation matching")
    print("=" * 60)

    map_file = "maps/ez_map.txt"
    if os.path.exists(map_file):
        verify_heuristic(map_file)
    else:
        print(f"Khong tim thay file: {map_file}")
