# heuristic.py
# Thanh vien A phu trach
# Ham heuristic cho A* (KHONG dung Manhattan/Euclidean)
#
# Phuong phap: BFS Distance + Permutation Matching
# - BFS tinh khoang cach thuc te giua box va goal (co tinh tuong)
# - Permutation tim cach ghep noi box-goal voi tong chi phi nho nhat

from collections import deque
import itertools


def calculate_heuristic(state, game_map):
    """
    Tinh gia tri heuristic cho 1 state.

    Phuong phap: BFS Distance + Permutation Matching

    Cac buoc:
    1. Tim cac box CHUA o goal va cac goal CHUA co box
    2. Tinh ma tran khoang cach BFS giua moi cap (box, goal)
    3. Dung Permutation tim ghep noi toi uu (tong chi phi nho nhat)
    4. Tra ve tong chi phi ghep noi

    Args:
        state: doi tuong State (co agent_pos va boxes)
        game_map: doi tuong GameMap (co walls, goals)

    Returns:
        int: gia tri heuristic (>= 0)
             0 neu da dat goal state
    """
    # Buoc 1: Tim boxes chua o goal va goals chua co box
    unmatched_boxes = [b for b in state.boxes if b not in game_map.goals]
    unmatched_goals = [g for g in game_map.goals if g not in state.boxes]

    # Buoc 2: Neu khong con box/goal chua ghep -> da xong
    if not unmatched_boxes:
        return 0

    n = len(unmatched_boxes)

    # Buoc 3: Tao ma tran cost bang BFS distance
    cost_matrix = []
    for box in unmatched_boxes:
        row = []
        for goal in unmatched_goals:
            dist = bfs_distance(box, goal, game_map)
            row.append(dist)
        cost_matrix.append(row)

    # Buoc 4: Tim ghep noi toi uu bang permutation
    # Voi so box nho (<= 7), O(n!) van chap nhan duoc (7! = 5040)
    min_cost = float('inf')
    for perm in itertools.permutations(range(n)):
        total = sum(cost_matrix[i][perm[i]] for i in range(n))
        if total < min_cost:
            min_cost = total

    return min_cost


def bfs_distance(start, end, game_map):
    """
    Tinh khoang cach ngan nhat tu start den end bang BFS.
    Chi di qua cac o KHONG phai tuong (khong quan tam box).

    Day la BFS chuan theo slide (trang 6):
    - frontier = FIFO queue (deque)
    - explored = set (visited)
    - Duyet 4 huong (N, S, E, W)

    Args:
        start: tuple (row, col) vi tri bat dau
        end: tuple (row, col) vi tri ket thuc
        game_map: doi tuong GameMap

    Returns:
        int: so buoc ngan nhat, hoac float('inf') neu khong den duoc
    """
    if start == end:
        return 0

    # frontier <- FIFO queue
    queue = deque([(start, 0)])
    # explored <- empty set
    visited = {start}

    # loop do
    while queue:
        pos, dist = queue.popleft()

        # Duyet 4 huong ke
        r, c = pos
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            neighbor = (nr, nc)

            # Chi di vao o khong phai tuong va chua visited
            if neighbor not in visited and game_map.is_free(neighbor):
                # if GOAL-TEST: tim thay dich
                if neighbor == end:
                    return dist + 1

                visited.add(neighbor)
                queue.append((neighbor, dist + 1))

    # return failure — khong den duoc
    return float('inf')


def is_deadlock(state, game_map):
    """
    Kiem tra state co bi deadlock khong (tuy chon nang cao).

    Deadlock = box khong the day den bat ky goal nao
    -> State nay vo vong, nen bo qua

    Kiem tra: CORNER DEADLOCK
    - Box co 2 mat bi chan boi tuong (1 ngang + 1 doc)
    - Va vi tri do KHONG phai goal
    -> Box bi ket vinh vien, khong the di chuyen

    Args:
        state: doi tuong State
        game_map: doi tuong GameMap

    Returns:
        True neu bi deadlock (nen bo qua state nay)
    """
    for box in state.boxes:
        if box not in game_map.goals:
            r, c = box
            wall_up    = game_map.is_wall((r - 1, c))
            wall_down  = game_map.is_wall((r + 1, c))
            wall_left  = game_map.is_wall((r, c - 1))
            wall_right = game_map.is_wall((r, c + 1))

            # Goc: 1 mat doc + 1 mat ngang deu la tuong
            if (wall_up or wall_down) and (wall_left or wall_right):
                return True

    return False
