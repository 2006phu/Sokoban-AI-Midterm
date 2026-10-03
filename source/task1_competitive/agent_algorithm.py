# agent_algorithm.py
# Thuat toan ra quyet dinh cho Agent 1 trong che do thi dau Sokoban
# Ket hop Breadth-First Search (tim duong) va Alpha-Beta Pruning (danh gia doi khang).
# Tich hop co che chong lap buoc (Anti-Oscillation), loai tru o chet (Deadlock Avoidance)
# va cuop hop chu dong. Gioi han thoi gian ra quyet dinh <= 1000ms moi buoc.

from collections import deque
import math
import time

DIRECTIONS = {
    "North": (-1, 0),
    "South": (1, 0),
    "East":  (0, 1),
    "West":  (0, -1)
}


def direction_name(dr, dc):
    for name, (r, c) in DIRECTIONS.items():
        if r == dr and c == dc:
            return name
    return "Stay"


def is_deadlock_cell(pos, goals, rows, cols):
    """
    Kiem tra o co phai o chet (deadlock) doc theo tuong bien khong chua goal:
    - O hang 1: Tuong tren cung (hang 0) la tuong -> khong the day hop xuong duoc
    - O hang rows-2: Tuong duoi cung la tuong -> khong the day hop len duoc
    - O cot 1: Tuong trai la tuong -> khong the day hop sang phai duoc
    - O cot cols-2: Tuong phai la tuong -> khong the day hop sang trai duoc
    """
    r, c = pos
    if pos in goals:
        return False
    if r == 1 and not any(g[0] == 1 for g in goals):
        return True
    if r == rows - 2 and not any(g[0] == rows - 2 for g in goals):
        return True
    if c == 1 and not any(g[1] == 1 for g in goals):
        return True
    if c == cols - 2 and not any(g[1] == cols - 2 for g in goals):
        return True
    return False


class Agent:
    """
    Agent 1 thi dau trong che do competitive.
    Ket hop Alpha-Beta Pruning, BFS Pathfinding, Chong lap buoc va Loai tru deadlock.
    """

    def __init__(self, agent_id=1):
        self.agent_id = agent_id
        self.contest_bias = 6
        self.target_box = None
        self.target_goal = None
        self.pos_history = deque(maxlen=24)
        self.blacklisted_boxes = {}
        self.standstill_count = 0
        self.steps_without_progress = 0
        self.last_boxes_snapshot = None

    def choose_action(self, game_state):
        """
        Ra quyet dinh hanh dong tiep theo trong vong <= 1000ms.
        """
        start_time = time.time()
        my_pos = game_state["my_pos"]
        opp_pos = game_state["opponent_pos"]
        walls = game_state["walls"]
        boxes = game_state["boxes"]
        goals = game_state["goals"]
        ownership = game_state.get("box_ownership", {})
        my_id = self.agent_id
        opp_id = 2 if my_id == 1 else 1
        steps_left = game_state.get("steps_remaining", 60)
        current_step = 200 - steps_left

        # ----------------------------------------------------
        # THEO DOI TIEN TRINH DAY HOP & PHAT HIEN LAP BUOC
        # ----------------------------------------------------
        boxes_tuple = tuple(sorted(boxes))
        if self.last_boxes_snapshot == boxes_tuple:
            self.steps_without_progress += 1
        else:
            self.steps_without_progress = 0
            self.last_boxes_snapshot = boxes_tuple

        if self.pos_history and my_pos == self.pos_history[-1]:
            self.standstill_count += 1
        else:
            self.standstill_count = 0

        is_oscillating = False
        if len(self.pos_history) >= 4:
            if self.pos_history[-1] == self.pos_history[-3] and self.pos_history[-2] == self.pos_history[-4]:
                is_oscillating = True
            elif self.pos_history.count(my_pos) >= 3:
                is_oscillating = True
        if self.standstill_count >= 2 or self.steps_without_progress >= 8:
            is_oscillating = True

        prev_pos = self.pos_history[-1] if self.pos_history else None
        self.pos_history.append(my_pos)

        # Neu bi kẹt hoac lap buoc: huy target va dua vao danh sach den tam thoi
        if is_oscillating:
            if self.target_box:
                self.blacklisted_boxes[self.target_box] = current_step + 12
            self.target_box = None
            self.target_goal = None
            self.steps_without_progress = 0

        # Don dep cac hop da het han danh sach den
        self.blacklisted_boxes = {b: exp for b, exp in self.blacklisted_boxes.items() if exp > current_step}

        rows = max(r for r, c in walls) + 1
        cols = max(c for r, c in walls) + 1

        # Loai bo cac hop da bi day vao o chet doc tuong khong the dua vao goal
        unplaced_boxes = [
            b for b in boxes 
            if b not in goals and b not in self.blacklisted_boxes and not is_deadlock_cell(b, goals, rows, cols)
        ]
        free_goals = [g for g in goals if g not in boxes]
        opp_boxes_on_goal = [b for b in boxes if b in goals and ownership.get(b) == opp_id and b not in self.blacklisted_boxes]

        dist_opp = abs(my_pos[0] - opp_pos[0]) + abs(my_pos[1] - opp_pos[1])
        my_score = game_state.get("my_boxes_on_goal", 0)
        opp_score = game_state.get("opponent_boxes_on_goal", 0)

        # ----------------------------------------------------
        # CHIEN LUOC 1: ALPHA-BETA SEARCH KHI CAN CHIEN (<= 2 O)
        # ----------------------------------------------------
        if dist_opp <= 2 and not is_oscillating and (time.time() - start_time < 0.8):
            act_ab = alpha_beta_search(game_state, self.agent_id, depth=2)
            if act_ab != "Stay":
                dr, dc = DIRECTIONS[act_ab]
                nxt = (my_pos[0] + dr, my_pos[1] + dc)
                if nxt not in walls and nxt != opp_pos:
                    if nxt not in boxes:
                        return act_ab
                    box_nxt = (nxt[0] + dr, nxt[1] + dc)
                    if box_nxt not in walls and box_nxt not in boxes and box_nxt != opp_pos:
                        return act_ab

        # ----------------------------------------------------
        # CHIEN LUOC 2: CUOP HOP CUA DOI THU (ACTIVE STEALING)
        # ----------------------------------------------------
        min_unplaced_dist = min(
            (abs(my_pos[0] - b[0]) + abs(my_pos[1] - b[1]) for b in unplaced_boxes),
            default=float('inf')
        )
        should_steal = opp_boxes_on_goal and (
            opp_score > my_score or
            len(unplaced_boxes) == 0 or
            any(abs(my_pos[0] - ob[0]) + abs(my_pos[1] - ob[1]) + 2 <= min_unplaced_dist for ob in opp_boxes_on_goal)
        )

        if should_steal:
            best_steal = None
            best_dist = float('inf')
            for ob in opp_boxes_on_goal:
                for name, (dr, dc) in DIRECTIONS.items():
                    dest = (ob[0] + dr, ob[1] + dc)
                    req_pos = (ob[0] - dr, ob[1] - dc)
                    if (dest not in walls and dest not in boxes and dest != opp_pos
                            and req_pos not in walls and req_pos not in boxes and req_pos != opp_pos):
                        path = self._bfs_path(my_pos, req_pos, walls, boxes | {opp_pos})
                        if path is not None:
                            d = len(path)
                            if d < best_dist:
                                best_dist = d
                                best_steal = (name, req_pos, path)
            if best_steal:
                act_name, req_pos, path = best_steal
                if my_pos == req_pos:
                    return act_name
                if path and len(path) > 0:
                    act = path[0]
                    dr, dc = DIRECTIONS[act]
                    nxt = (my_pos[0] + dr, my_pos[1] + dc)
                    if not (is_oscillating and nxt == prev_pos) and nxt != opp_pos:
                        return act

        # ----------------------------------------------------
        # CHIEN LUOC 3: DAY HOP TRUNG LAP VAO GOAL (TRANH O CHET)
        # ----------------------------------------------------
        if unplaced_boxes and free_goals:
            if self.target_box not in unplaced_boxes or self.target_goal not in free_goals:
                self.target_box = None
                self.target_goal = None

            if self.target_box is None:
                best_pair = None
                best_val = float('inf')
                for b in unplaced_boxes:
                    d_a = abs(my_pos[0] - b[0]) + abs(my_pos[1] - b[1])
                    d_o = abs(opp_pos[0] - b[0]) + abs(opp_pos[1] - b[1])
                    penalty = self.contest_bias if d_o < d_a else 0
                    for g in free_goals:
                        d_g = abs(b[0] - g[0]) + abs(b[1] - g[1])
                        val = d_a + 2 * d_g + penalty
                        if val < best_val:
                            best_val = val
                            best_pair = (b, g)
                if best_pair:
                    self.target_box, self.target_goal = best_pair

            if self.target_box:
                tb = self.target_box
                tg = self.target_goal
                candidate_pushes = []
                for name, (dr, dc) in DIRECTIONS.items():
                    dest = (tb[0] + dr, tb[1] + dc)
                    req_pos = (tb[0] - dr, tb[1] - dc)
                    # Khong bao gio day hop vao o chet deadlock
                    if is_deadlock_cell(dest, goals, rows, cols):
                        continue
                    if (dest not in walls and dest not in boxes and dest != opp_pos
                            and req_pos not in walls and req_pos not in boxes and req_pos != opp_pos):
                        d = abs(dest[0] - tg[0]) + abs(dest[1] - tg[1])
                        path = self._bfs_path(my_pos, req_pos, walls, boxes | {opp_pos})
                        if path is not None:
                            candidate_pushes.append((d, len(path), name, req_pos, path))

                if candidate_pushes:
                    candidate_pushes.sort(key=lambda x: (x[0], x[1]))
                    for _, _, act_name, req_pos, path in candidate_pushes:
                        if my_pos == req_pos:
                            return act_name
                        if path and len(path) > 0:
                            act = path[0]
                            dr, dc = DIRECTIONS[act]
                            nxt = (my_pos[0] + dr, my_pos[1] + dc)
                            if not (is_oscillating and nxt == prev_pos) and nxt != opp_pos:
                                return act
                else:
                    self.blacklisted_boxes[self.target_box] = current_step + 6
                    self.target_box = None
                    self.target_goal = None

        # ----------------------------------------------------
        # CHIEN LUOC 4: DI VONG NE VA CHAM (DETOUR FALLBACK)
        # ----------------------------------------------------
        for name, (dr, dc) in DIRECTIONS.items():
            nxt = (my_pos[0] + dr, my_pos[1] + dc)
            if nxt not in walls and nxt not in boxes and nxt != opp_pos:
                if not (is_oscillating and nxt == prev_pos):
                    return name

        return "Stay"

    def _bfs_path(self, start, target, walls, avoid):
        """
        Dua tren ma gia BREADTH-FIRST-SEARCH tim duong di ngan nhat:
        - node <- a node with STATE = start, PATH-COST = 0
        - if problem.GOAL-TEST(node.STATE) then return SOLUTION(node)
        - frontier <- a FIFO queue with node as the only element
        - explored <- an empty set
        """
        if start == target:
            return []

        frontier = deque([(start, [])])
        explored = {start}

        while frontier:
            curr, path = frontier.popleft()
            for name, (dr, dc) in DIRECTIONS.items():
                nxt = (curr[0] + dr, curr[1] + dc)
                if nxt not in explored and nxt not in walls and (nxt not in avoid or nxt == target):
                    new_path = path + [name]
                    if nxt == target:
                        return new_path
                    explored.add(nxt)
                    frontier.append((nxt, new_path))
        return None


# ============================================================
# ALPHA-BETA PRUNING SEARCH
# ============================================================
def alpha_beta_search(game_state, agent_id, depth=2):
    """
    Ma gia ALPHA-BETA-SEARCH:
    v <- MAX-VALUE(state, -inf, +inf)
    return the action in ACTIONS(state) with value v
    """
    alpha = -math.inf
    beta = math.inf
    best_action = "Stay"
    best_value = -math.inf

    actions = ["North", "South", "East", "West", "Stay"]
    for action in actions:
        next_state = _result(game_state, action, agent_id)
        val = min_value(next_state, alpha, beta, depth - 1, agent_id)
        if val > best_value:
            best_value = val
            best_action = action
        alpha = max(alpha, best_value)

    return best_action


def max_value(state, alpha, beta, depth, agent_id):
    """
    Ma gia MAX-VALUE(state, alpha, beta)
    """
    if depth <= 0:
        return utility(state, agent_id)

    v = -math.inf
    actions = ["North", "South", "East", "West", "Stay"]
    for action in actions:
        next_state = _result(state, action, agent_id)
        v = max(v, min_value(next_state, alpha, beta, depth - 1, agent_id))
        if v >= beta:
            return v
        alpha = max(alpha, v)
    return v


def min_value(state, alpha, beta, depth, agent_id):
    """
    Ma gia MIN-VALUE(state, alpha, beta)
    """
    if depth <= 0:
        return utility(state, agent_id)

    v = math.inf
    opponent_id = 2 if agent_id == 1 else 1
    actions = ["North", "South", "East", "West", "Stay"]
    for action in actions:
        next_state = _result(state, action, opponent_id)
        v = min(v, max_value(next_state, alpha, beta, depth - 1, agent_id))
        if v <= alpha:
            return v
        beta = min(beta, v)
    return v


def utility(state, agent_id):
    """
    Ham tien ich Utility danh gia trang thai doi khang:
    U = (Diem_cua_minh * 20 - Khoang_cach_toi_dich) - (Diem_doi_thu * 20)
    """
    my_score = state.get("my_boxes_on_goal", 0)
    opp_score = state.get("opponent_boxes_on_goal", 0)
    my_pos = state.get("my_pos", (0, 0))
    goals = state.get("goals", set())

    min_dist_to_goal = min(
        (abs(my_pos[0] - g[0]) + abs(my_pos[1] - g[1]) for g in goals),
        default=0
    )
    return (my_score * 20 - min_dist_to_goal) - (opp_score * 20)


def _result(state, action, agent_id):
    """
    Mo phong trang thai tiep theo khi thuc hien action.
    Tranh di xuyen qua tuong, hop bi chan, hoac doi thu.
    """
    dr, dc = DIRECTIONS.get(action, (0, 0))
    is_me = (agent_id == state.get("my_id", 1))
    my_pos = state.get("my_pos", (0, 0))
    opp_pos = state.get("opponent_pos", (0, 0))
    walls = state.get("walls", set())
    boxes = set(state.get("boxes", set()))

    curr = my_pos if is_me else opp_pos
    other = opp_pos if is_me else my_pos
    nxt = (curr[0] + dr, curr[1] + dc)

    if nxt in walls or nxt == other or action == "Stay":
        return dict(state)

    new_boxes = set(boxes)
    if nxt in boxes:
        box_nxt = (nxt[0] + dr, nxt[1] + dc)
        if box_nxt in walls or box_nxt in boxes or box_nxt == other:
            return dict(state)
        new_boxes.remove(nxt)
        new_boxes.add(box_nxt)

    res = dict(state)
    res["boxes"] = new_boxes
    if is_me:
        res["my_pos"] = nxt
    else:
        res["opponent_pos"] = nxt
    return res
