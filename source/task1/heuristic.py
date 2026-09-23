# heuristic.py
# Thanh vien A phu trach
# Ham heuristic cho A* (KHONG dung Manhattan/Euclidean)

from collections import deque

def calculate_heuristic(state, game_map):
    """
    Tinh gia tri heuristic cho 1 state.

    Phuong phap: BFS Distance + Hungarian Algorithm

    Cac buoc:
    1. Tim cac box CHUA o goal va cac goal CHUA co box
    2. Tinh ma tran khoang cach BFS giua moi cap (box, goal)
    3. Dung Hungarian Algorithm tim ghep noi toi uu
    4. Tra ve tong chi phi ghep noi

    Args:
        state: doi tuong State (co agent_pos va boxes)
        game_map: doi tuong GameMap (co walls, goals)

    Returns:
        int: gia tri heuristic (>= 0)
             0 neu da dat goal state
    """
    # TODO: Implement heuristic

    # Buoc 1: Tim boxes chua o goal va goals chua co box
    # unmatched_boxes = [b for b in state.boxes if b not in game_map.goals]
    # unmatched_goals = [g for g in game_map.goals if g not in state.boxes]
    #
    # Buoc 2: Neu khong con box/goal chua ghep -> return 0
    #
    # Buoc 3: Tao ma tran cost bang BFS
    # cost_matrix[i][j] = bfs_distance(unmatched_boxes[i], unmatched_goals[j])
    #
    # Buoc 4: Ap dung Hungarian Algorithm
    # Tu scipy: from scipy.optimize import linear_sum_assignment
    # row_ind, col_ind = linear_sum_assignment(cost_matrix)
    # total = sum(cost_matrix[r][c] for r, c in zip(row_ind, col_ind))
    #
    # Buoc 5: return total
    pass


def bfs_distance(start, end, game_map):
    """
    Tinh khoang cach ngan nhat tu start den end bang BFS.
    Chi di qua cac o KHONG phai tuong.

    Args:
        start: tuple (row, col) vi tri bat dau
        end: tuple (row, col) vi tri ket thuc
        game_map: doi tuong GameMap

    Returns:
        int: so buoc ngan nhat, hoac vo cuc neu khong den duoc

    Goi y:
    - Dung deque (hang doi 2 dau) de lam queue BFS
    - Duyet 4 huong (N, S, E, W)
    - Dung set visited de tranh lap
    - KHONG can quan tam den box, chi tinh duong di tren ban do trong
    """
    # TODO: Implement BFS tinh khoang cach
    # Buoc 1: Khoi tao queue = deque([(start, 0)]), visited = {start}
    # Buoc 2: While queue khong rong:
    #   - Pop (pos, dist) tu dau queue
    #   - Neu pos == end -> return dist
    #   - Duyet 4 huong ke
    #   - Neu o ke khong phai tuong va chua visited -> them vao queue
    # Buoc 3: Neu het queue ma chua tim thay -> return float('inf')
    pass


def is_deadlock(state, game_map):
    """
    Kiem tra state co bi deadlock khong (tuy chon nhung nen lam).

    Deadlock = box khong the day den bat ky goal nao
    -> State nay vo vong, nen bo qua

    Kiem tra don gian: CORNER DEADLOCK
    - Box co 2 mat bi chan boi tuong (1 ngang + 1 doc)
    - Va vi tri do KHONG phai goal

    Args:
        state: doi tuong State
        game_map: doi tuong GameMap

    Returns:
        True neu bi deadlock (nen bo qua state nay)
    """
    # TODO: Kiem tra deadlock
    # Voi moi box trong state.boxes:
    #   Neu box KHONG phai goal:
    #     Kiem tra 4 goc:
    #       (tuong o tren VA tuong o trai) -> deadlock
    #       (tuong o tren VA tuong o phai) -> deadlock
    #       (tuong o duoi VA tuong o trai) -> deadlock
    #       (tuong o duoi VA tuong o phai) -> deadlock
    pass
