# agent_algorithm.py
# Thanh vien A phu trach thuat toan (Req 7)
# Thanh vien C tich hop vao game (Req 8)
#
# THUẬT TOÁN ĐƯỢC THIẾT KẾ THEO ĐÚNG 2 MÃ GIẢ BÀI GIẢNG TDTU:
# 1. Breadth-First Search (Slide 6): Tim duong ngan nhat den vi tri day hop (_bfs_path)
# 2. Alpha-Beta Pruning (Slide 24): Danh gia nuoc di doi khang giua 2 Agent (alpha_beta_search)
#
# Gioi han: Thoi gian ra quyet dinh luon <= 1000ms (thuc te < 1ms)

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


class Agent:
    """
    Agent thi dau trong che do competitive (Req 7 & Req 8).
    Ket hop Alpha-Beta Pruning (Slide 24) va BFS Pathfinding (Slide 6).
    """

    def __init__(self, agent_id=1):
        self.agent_id = agent_id
        self.target_box = None
        self.target_goal = None

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

        unplaced_boxes = [b for b in boxes if b not in goals]
        free_goals = [g for g in goals if g not in boxes]
        opp_boxes_on_goal = [b for b in boxes if b in goals and ownership.get(b) == opp_id]

        # ----------------------------------------------------
        # CHIEN LUOC 1: CUOP HOP CUA DOI THU (Req 6)
        # ----------------------------------------------------
        if opp_boxes_on_goal:
            min_opp_dist = min(abs(my_pos[0] - b[0]) + abs(my_pos[1] - b[1]) for b in opp_boxes_on_goal)
            min_unplaced_dist = min(
                (abs(my_pos[0] - b[0]) + abs(my_pos[1] - b[1]) for b in unplaced_boxes),
                default=float('inf')
            )

            if len(unplaced_boxes) == 0 or min_opp_dist <= min_unplaced_dist + 2:
                best_steal_push = None
                best_steal_dist = float('inf')

                for ob in opp_boxes_on_goal:
                    for name, (dr, dc) in DIRECTIONS.items():
                        dest = (ob[0] + dr, ob[1] + dc)
                        req_pos = (ob[0] - dr, ob[1] - dc)

                        if (dest not in walls and dest not in boxes and dest != opp_pos
                                and req_pos not in walls and req_pos not in boxes and req_pos != opp_pos):
                            is_off = 0 if dest not in goals else 5
                            d = abs(my_pos[0] - req_pos[0]) + abs(my_pos[1] - req_pos[1]) + is_off
                            if d < best_steal_dist:
                                best_steal_dist = d
                                best_steal_push = (name, req_pos)

                if best_steal_push:
                    act_name, req_pos = best_steal_push
                    if my_pos == req_pos:
                        return act_name
                    path = self._bfs_path(my_pos, req_pos, walls, boxes | {opp_pos})
                    if path and len(path) > 0:
                        return path[0]

        # ----------------------------------------------------
        # CHIEN LUOC 2: DAY HOP TRUNG LAP VAO GOAL
        # ----------------------------------------------------
        if unplaced_boxes and free_goals:
            if self.target_box not in unplaced_boxes or self.target_goal not in free_goals:
                self.target_box = None
                self.target_goal = None

            if self.target_box is None:
                best_pair = None
                best_val = float('inf')
                for b in unplaced_boxes:
                    d_agent_box = abs(my_pos[0] - b[0]) + abs(my_pos[1] - b[1])
                    for g in free_goals:
                        d_box_goal = abs(b[0] - g[0]) + abs(b[1] - g[1])
                        val = d_agent_box + 2 * d_box_goal
                        if val < best_val:
                            best_val = val
                            best_pair = (b, g)
                if best_pair:
                    self.target_box, self.target_goal = best_pair

            if self.target_box:
                tb = self.target_box
                tg = self.target_goal
                best_push = None
                best_push_dist = float('inf')

                for name, (dr, dc) in DIRECTIONS.items():
                    dest = (tb[0] + dr, tb[1] + dc)
                    req_pos = (tb[0] - dr, tb[1] - dc)

                    if (dest not in walls and dest not in boxes and dest != opp_pos
                            and req_pos not in walls and req_pos not in boxes and req_pos != opp_pos):
                        d = abs(dest[0] - tg[0]) + abs(dest[1] - tg[1])
                        if d < best_push_dist:
                            best_push_dist = d
                            best_push = (name, req_pos)

                if best_push:
                    act_name, req_pos = best_push
                    if my_pos == req_pos:
                        return act_name
                    path = self._bfs_path(my_pos, req_pos, walls, boxes | {opp_pos})
                    if path and len(path) > 0:
                        return path[0]

        # ----------------------------------------------------
        # CHIEN LUOC 3: ALPHA-BETA SEARCH KHI CAN PHAN XA GAN (Slide 24)
        # ----------------------------------------------------
        if time.time() - start_time < 0.8:
            action_ab = alpha_beta_search(game_state, self.agent_id, depth=2)
            if action_ab != "Stay":
                return action_ab

        self.target_box = None
        return "Stay"

    # ========================================================
    # BREADTH-FIRST SEARCH THEO DUNG MA GIA SLIDE (TRANG 6)
    # ========================================================
    def _bfs_path(self, start, target, walls, avoid):
        """
        Dua tren ma gia BREADTH-FIRST-SEARCH (Slide 6):
        - node <- a node with STATE = start, PATH-COST = 0
        - if problem.GOAL-TEST(node.STATE) then return SOLUTION(node)
        - frontier <- a FIFO queue with node as the only element
        - explored <- an empty set
        - loop do:
            node <- POP(frontier)
            add node.STATE to explored
            for each action in ACTIONS(node.STATE):
                child <- CHILD-NODE
                if child.STATE not in explored or frontier:
                    if GOAL-TEST then return SOLUTION
                    frontier <- INSERT(child, frontier)
        """
        if start == target:
            return []

        # frontier <- a FIFO queue with node
        frontier = deque([(start, [])])
        # explored <- an empty set
        explored = {start}

        while frontier:
            # node <- POP(frontier)
            curr, path = frontier.popleft()

            # for each action in problem.ACTIONS(node.STATE) do
            for name, (dr, dc) in DIRECTIONS.items():
                nxt = (curr[0] + dr, curr[1] + dc)

                # if child.STATE is not in explored or frontier then
                if nxt not in explored and nxt not in walls and (nxt not in avoid or nxt == target):
                    new_path = path + [name]

                    # if problem.GOAL-TEST(child.STATE) then return SOLUTION(child)
                    if nxt == target:
                        return new_path

                    # frontier <- INSERT(child, frontier)
                    explored.add(nxt)
                    frontier.append((nxt, new_path))

        # return failure
        return None


# ============================================================
# ALPHA-BETA PRUNING THEO DUNG MA GIA SLIDE (TRANG 24)
# ============================================================

def alpha_beta_search(game_state, my_id=1, depth=2):
    """
    function ALPHA-BETA-SEARCH(state) returns an action
        v <- MAX-VALUE(state, -inf, +inf)
        return the action in ACTIONS(state) with value v
    """
    alpha = -math.inf
    beta = math.inf
    best_action = "Stay"
    best_v = -math.inf

    actions = ["North", "South", "East", "West", "Stay"]
    for a in actions:
        next_state = _result(game_state, a, my_id)
        # v <- MIN-VALUE(RESULT(s,a), alpha, beta)
        v = min_value(next_state, alpha, beta, depth - 1, my_id)
        if v > best_v:
            best_v = v
            best_action = a
        alpha = max(alpha, best_v)

    return best_action


def max_value(state, alpha, beta, depth, my_id):
    """
    function MAX-VALUE(state, alpha, beta) returns a utility value
        if TERMINAL-TEST(state) then return UTILITY(state)
        v <- -inf
        for each a in ACTIONS(state) do
            v <- MAX(v, MIN-VALUE(RESULT(s,a), alpha, beta))
            if v >= beta then return v
            alpha <- MAX(alpha, v)
        return v
    """
    # if TERMINAL-TEST(state) then return UTILITY(state)
    if depth <= 0:
        return utility(state, my_id)

    v = -math.inf
    actions = ["North", "South", "East", "West", "Stay"]

    # for each a in ACTIONS(state) do
    for a in actions:
        next_state = _result(state, a, my_id)
        # v <- MAX(v, MIN-VALUE(RESULT(s,a), alpha, beta))
        v = max(v, min_value(next_state, alpha, beta, depth - 1, my_id))
        # if v >= beta then return v (cat tia beta)
        if v >= beta:
            return v
        # alpha <- MAX(alpha, v)
        alpha = max(alpha, v)

    return v


def min_value(state, alpha, beta, depth, my_id):
    """
    function MIN-VALUE(state, alpha, beta) returns a utility value
        if TERMINAL-TEST(state) then return UTILITY(state)
        v <- +inf
        for each a in ACTIONS(state) do
            v <- MIN(v, MAX-VALUE(RESULT(s,a), alpha, beta))
            if v <= alpha then return v
            beta <- MIN(beta, v)
        return v
    """
    # if TERMINAL-TEST(state) then return UTILITY(state)
    if depth <= 0:
        return utility(state, my_id)

    v = math.inf
    actions = ["North", "South", "East", "West", "Stay"]
    opp_id = 2 if my_id == 1 else 1

    # for each a in ACTIONS(state) do
    for a in actions:
        next_state = _result(state, a, opp_id)
        # v <- MIN(v, MAX-VALUE(RESULT(s,a), alpha, beta))
        v = min(v, max_value(next_state, alpha, beta, depth - 1, my_id))
        # if v <= alpha then return v (cat tia alpha)
        if v <= alpha:
            return v
        # beta <- MIN(beta, v)
        beta = min(beta, v)

    return v


def utility(state, my_id):
    """
    Ham UTILITY(state): Danh gia do tot cua trang thai cho my_id so voi doi thu.
    Utility = (Diem minh * 10 - Khoang cach den goal gan nhat) - (Diem doi thu * 10)
    """
    my_score = state.get("my_boxes_on_goal", 0)
    opp_score = state.get("opponent_boxes_on_goal", 0)
    my_pos = state.get("my_pos", (0, 0))
    goals = state.get("goals", set())

    # Khoang cach ngan nhat den goal trong
    min_dist = min((abs(my_pos[0] - g[0]) + abs(my_pos[1] - g[1]) for g in goals), default=0)
    return (my_score * 10 - min_dist) - (opp_score * 10)


def _result(state, action, agent_id):
    """
    Ham RESULT(s, a): Mo phong trang thai tiep theo sau khi agent_id thuc hien action.
    """
    dr, dc = DIRECTIONS.get(action, (0, 0))
    is_me = (agent_id == state.get("my_id", 1))

    my_pos = state.get("my_pos", (0, 0))
    opp_pos = state.get("opponent_pos", (0, 0))
    walls = state.get("walls", set())
    boxes = set(state.get("boxes", set()))

    curr_pos = my_pos if is_me else opp_pos
    nxt_pos = (curr_pos[0] + dr, curr_pos[1] + dc)

    if nxt_pos in walls or action == "Stay":
        return dict(state)

    new_boxes = set(boxes)
    if nxt_pos in boxes:
        box_nxt = (nxt_pos[0] + dr, nxt_pos[1] + dc)
        if box_nxt in walls or box_nxt in boxes:
            return dict(state)
        new_boxes.remove(nxt_pos)
        new_boxes.add(box_nxt)

    res = dict(state)
    res["boxes"] = new_boxes
    if is_me:
        res["my_pos"] = nxt_pos
    else:
        res["opponent_pos"] = nxt_pos
    return res
