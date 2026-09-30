# heuristic.py
# Thanh vien A phu trach
# Ham heuristic cho A* (KHONG dung Manhattan/Euclidean)
#
# Phuong phap: BFS Distance + Optimal Assignment
# - Precompute BFS distance tu moi goal den tat ca cac o (1 lan duy nhat)
# - Hungarian Algorithm (scipy) hoac greedy matching
# - Deadlock detection de cat tia som

from collections import deque


class HeuristicCalculator:
    """
    Tinh heuristic voi BFS distance duoc precompute.
    Tao 1 lan, dung lai nhieu lan -> nhanh hon gap nhieu.
    """

    def __init__(self, game_map):
        self.game_map = game_map
        # Precompute: BFS distance tu MOI GOAL den tat ca cac o tren ban do
        # dist_from_goal[goal_pos] = {pos: distance}
        self.dist_from_goal = {}
        for goal in game_map.goals:
            self.dist_from_goal[goal] = self._bfs_all(goal)

        # Thu import scipy de dung Hungarian (nhanh hon permutation)
        self._use_scipy = False
        try:
            from scipy.optimize import linear_sum_assignment
            self._linear_sum_assignment = linear_sum_assignment
            self._use_scipy = True
        except ImportError:
            pass

    def _bfs_all(self, start):
        """
        BFS tu start den TAT CA cac o tren ban do.
        Tra ve dict {pos: distance}.
        Chi can chay 1 lan cho moi goal.
        """
        dist = {start: 0}
        queue = deque([start])

        while queue:
            pos = queue.popleft()
            r, c = pos
            d = dist[pos]
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                neighbor = (r + dr, c + dc)
                if neighbor not in dist and self.game_map.is_free(neighbor):
                    dist[neighbor] = d + 1
                    queue.append(neighbor)

        return dist

    def calculate(self, state):
        """
        Tinh heuristic cho 1 state.
        Tra ve 0 neu da dat goal state.
        Tra ve float('inf') neu deadlock.
        """
        # Kiem tra deadlock truoc (rat nhanh)
        if self._is_deadlock(state):
            return float('inf')

        # Tim boxes chua o goal va goals chua co box
        unmatched_boxes = [b for b in state.boxes if b not in self.game_map.goals]
        unmatched_goals = [g for g in self.game_map.goals if g not in state.boxes]

        if not unmatched_boxes:
            return 0

        n = len(unmatched_boxes)

        # Tao ma tran cost tu precomputed BFS distances (O(1) lookup)
        cost_matrix = []
        for box in unmatched_boxes:
            row = []
            for goal in unmatched_goals:
                # Tra cuu tu bang da tinh san
                d = self.dist_from_goal[goal].get(box, float('inf'))
                if d == float('inf'):
                    return float('inf')  # Box khong the den goal nay
                row.append(d)
            cost_matrix.append(row)

        # Tim ghep noi toi uu
        if self._use_scipy:
            # Hungarian Algorithm O(n^3) — nhanh nhat
            import numpy as np
            cost_np = np.array(cost_matrix)
            row_ind, col_ind = self._linear_sum_assignment(cost_np)
            return int(cost_np[row_ind, col_ind].sum())
        elif n <= 8:
            # Permutation O(n!) — chap nhan duoc khi n nho
            import itertools
            min_cost = float('inf')
            for perm in itertools.permutations(range(n)):
                total = sum(cost_matrix[i][perm[i]] for i in range(n))
                if total < min_cost:
                    min_cost = total
            return min_cost
        else:
            # Greedy matching cho n lon
            return self._greedy_match(cost_matrix, n)

    def _greedy_match(self, cost_matrix, n):
        """Greedy matching O(n^2) — nhanh nhung khong toi uu."""
        used_goals = set()
        total = 0
        for i in range(n):
            best_j = -1
            best_cost = float('inf')
            for j in range(n):
                if j not in used_goals and cost_matrix[i][j] < best_cost:
                    best_cost = cost_matrix[i][j]
                    best_j = j
            if best_j >= 0:
                used_goals.add(best_j)
                total += best_cost
            else:
                return float('inf')
        return total

    def _is_deadlock(self, state):
        """
        Kiem tra deadlock nhanh.
        Corner deadlock: box khong o goal + 2 mat ke la tuong (1 doc + 1 ngang).
        """
        for box in state.boxes:
            if box not in self.game_map.goals:
                r, c = box
                wall_up    = self.game_map.is_wall((r - 1, c))
                wall_down  = self.game_map.is_wall((r + 1, c))
                wall_left  = self.game_map.is_wall((r, c - 1))
                wall_right = self.game_map.is_wall((r, c + 1))
                if (wall_up or wall_down) and (wall_left or wall_right):
                    return True
        return False


# ============================================================
# HAM WRAPPER (tuong thich voi code cu)
# ============================================================

# Cache de khong tao lai HeuristicCalculator moi lan
_calculator_cache = {}


def calculate_heuristic(state, game_map):
    """
    Ham wrapper de tuong thich voi cach goi cu.
    Tu dong cache HeuristicCalculator theo game_map.
    """
    map_id = id(game_map)
    if map_id not in _calculator_cache:
        _calculator_cache[map_id] = HeuristicCalculator(game_map)
    return _calculator_cache[map_id].calculate(state)


def bfs_distance(start, end, game_map):
    """BFS tinh khoang cach (giu lai de tuong thich)."""
    if start == end:
        return 0
    queue = deque([(start, 0)])
    visited = {start}
    while queue:
        pos, dist = queue.popleft()
        r, c = pos
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            neighbor = (r + dr, c + dc)
            if neighbor not in visited and game_map.is_free(neighbor):
                if neighbor == end:
                    return dist + 1
                visited.add(neighbor)
                queue.append((neighbor, dist + 1))
    return float('inf')


def is_deadlock(state, game_map):
    """Kiem tra deadlock (giu lai de tuong thich)."""
    for box in state.boxes:
        if box not in game_map.goals:
            r, c = box
            wall_up    = game_map.is_wall((r - 1, c))
            wall_down  = game_map.is_wall((r + 1, c))
            wall_left  = game_map.is_wall((r, c - 1))
            wall_right = game_map.is_wall((r, c + 1))
            if (wall_up or wall_down) and (wall_left or wall_right):
                return True
    return False
