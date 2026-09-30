# agent_algorithm.py
# Thanh vien A phu trach thuat toan (Req 7)
# Thanh vien C tich hop vao game (Req 8)
#
# FILE NAY PHAI TACH RIENG de cac nhom co the thi dau voi nhau
# Moi nhom viet 1 agent_algorithm.py rieng
#
# Thuat toan su dung:
# - GBFS (Greedy Best-First Search) de chon muc tieu nhanh
# - BFS pathfinding (theo ma gia slide trang 6) de tim duong di
# - Alpha-Beta pruning (theo ma gia slide trang 24) cho quyet dinh nang cao
#
# Gioi han: moi quyet dinh phai tra ve trong 1000ms

from collections import deque
import time


# 4 huong di chuyen va ten tuong ung
DIRECTIONS = {
    "North": (-1, 0),
    "South": (1, 0),
    "East":  (0, 1),
    "West":  (0, -1)
}


def direction_name(dr, dc):
    """Chuyen (dr, dc) thanh ten huong."""
    for name, (r, c) in DIRECTIONS.items():
        if r == dr and c == dc:
            return name
    return "Stay"


class Agent:
    """
    Agent thi dau trong che do competitive.

    Chien luoc: GBFS (Greedy Best-First Search)
    - Tim goal trong gan nhat
    - Tim box gan nhat co the day den goal do
    - Tim vi tri dung de day box
    - BFS tim duong den vi tri day
    - Tra ve buoc tiep theo

    Attributes:
        agent_id:   0 hoac 1 (phan biet 2 agent)
    """

    def __init__(self, agent_id):
        self.agent_id = agent_id

    def choose_action(self, game_state):
        """
        Chon hanh dong tiep theo.

        GIOI HAN: Phai tra ve trong 1000ms.

        Chien luoc GBFS:
        1. Tim goal trong gan nhat (khong co box cua minh)
        2. Tim box gan nhat co the day den goal do
        3. Xac dinh vi tri can dung de day box
        4. BFS tim duong den vi tri do
        5. Neu da o vi tri day -> day box
        6. Tra ve buoc dau tien cua duong di

        Args:
            game_state: dict chua thong tin hien tai
                {
                    "my_pos": (row, col),
                    "opponent_pos": (row, col),
                    "boxes": set of (row, col),
                    "my_boxes_on_goal": int,
                    "opponent_boxes_on_goal": int,
                    "goals": set of (row, col),
                    "walls": set of (row, col),
                    "steps_remaining": int,
                }

        Returns:
            string: "North", "South", "East", "West", hoac "Stay"
        """
        start_time = time.time()
        my_pos = game_state["my_pos"]
        walls = game_state["walls"]
        boxes = game_state["boxes"]
        goals = game_state["goals"]
        opponent_pos = game_state["opponent_pos"]

        # Tap cac o bi chan (tuong + box + doi thu)
        obstacles = walls | boxes | {opponent_pos}

        # Buoc 1: Tim goal trong gan nhat
        target_goal = self._find_nearest_free_goal(my_pos, goals, boxes, walls)
        if target_goal is None:
            return "Stay"

        # Buoc 2: Tim box gan nhat co the day den target_goal
        target_box = self._find_nearest_box(my_pos, boxes, target_goal, walls)
        if target_box is None:
            return "Stay"

        # Buoc 3: Tim vi tri day (dung phia doi dien huong day)
        push_pos = self._find_push_position(
            target_box, target_goal, walls, boxes, opponent_pos
        )
        if push_pos is None:
            # Khong co vi tri day hop le -> thu di ve phia box
            path = self._bfs_path(my_pos, target_box, walls, {opponent_pos})
            if path and len(path) > 1:
                return path[0]
            return "Stay"

        # Buoc 4: Kiem tra da o vi tri day chua
        if my_pos == push_pos:
            # Da o vi tri day -> day box (di ve huong box)
            dr = target_box[0] - my_pos[0]
            dc = target_box[1] - my_pos[1]
            return direction_name(dr, dc)

        # Buoc 5: BFS tim duong den vi tri day
        # Tranh di vao box va doi thu
        avoid = boxes | {opponent_pos}
        path = self._bfs_path(my_pos, push_pos, walls, avoid)

        # Dam bao khong vuot 1000ms
        if time.time() - start_time > 0.9:
            return "Stay"

        if path and len(path) > 0:
            return path[0]

        # Fallback: thu di ve huong goal
        return self._move_toward(my_pos, target_goal, walls, obstacles)

    # ========================================================
    # TIM GOAL TRONG GAN NHAT
    # ========================================================
    def _find_nearest_free_goal(self, my_pos, goals, boxes, walls):
        """
        Tim goal gan nhat chua co box.
        Dung BFS de tinh khoang cach thuc te (co tinh tuong).

        Anh xa tu ma gia BFS slide (trang 6):
        - frontier = FIFO queue (deque)
        - explored = empty set
        - POP -> kiem tra goal test -> INSERT neighbors

        Returns:
            tuple (row, col) hoac None
        """
        # BFS tu my_pos, tim goal trong dau tien gap duoc
        queue = deque([(my_pos, 0)])
        visited = {my_pos}

        best_goal = None
        best_dist = float('inf')

        while queue:
            pos, dist = queue.popleft()

            # Goal test: o nay la goal va chua co box
            if pos in goals and pos not in boxes:
                if dist < best_dist:
                    best_dist = dist
                    best_goal = pos
                    return best_goal  # BFS dam bao day la gan nhat

            r, c = pos
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                neighbor = (r + dr, c + dc)
                if neighbor not in visited and neighbor not in walls:
                    visited.add(neighbor)
                    queue.append((neighbor, dist + 1))

        return best_goal

    # ========================================================
    # TIM BOX GAN NHAT
    # ========================================================
    def _find_nearest_box(self, my_pos, boxes, target_goal, walls):
        """
        Tim box gan agent nhat (BFS distance).

        Returns:
            tuple (row, col) hoac None
        """
        best_box = None
        best_dist = float('inf')

        for box in boxes:
            # Tinh BFS distance tu agent den box
            dist = self._bfs_distance(my_pos, box, walls, set())
            if dist < best_dist:
                best_dist = dist
                best_box = box

        return best_box

    # ========================================================
    # TIM VI TRI DAY
    # ========================================================
    def _find_push_position(self, box_pos, target_goal, walls, boxes, opp_pos):
        """
        Tim vi tri agent can dung de day box ve phia goal.

        Logic:
        - Xac dinh huong tu box den goal
        - Vi tri day = phia doi dien (sau lung box)
        - Kiem tra vi tri do co trong va hop le khong

        Returns:
            tuple (row, col) vi tri can dung, hoac None
        """
        br, bc = box_pos
        gr, gc = target_goal

        # Thu cac huong day co the
        possible_pushes = []

        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            # Vi tri box se den neu day theo huong (dr, dc)
            new_box = (br + dr, bc + dc)
            # Vi tri agent can dung (phia doi dien)
            agent_pos = (br - dr, bc - dc)

            # Kiem tra:
            # 1. Vi tri box moi khong la tuong, khong co box khac
            # 2. Vi tri agent dung khong la tuong, khong co box, khong co doi thu
            if (new_box not in walls and new_box not in boxes
                    and agent_pos not in walls and agent_pos not in boxes
                    and agent_pos != opp_pos):
                # Tinh khoang cach tu new_box den goal (uoc tinh)
                box_to_goal = abs(new_box[0] - gr) + abs(new_box[1] - gc)
                possible_pushes.append((box_to_goal, agent_pos))

        if not possible_pushes:
            return None

        # Chon vi tri day tot nhat (box gan goal nhat sau khi day)
        possible_pushes.sort()
        return possible_pushes[0][1]

    # ========================================================
    # BFS TIM DUONG - THEO MA GIA SLIDE (TRANG 6)
    # ========================================================
    def _bfs_path(self, start, end, walls, avoid):
        """
        Tim duong ngan nhat tu start den end, tranh walls va avoid.

        Anh xa truc tiep tu ma gia BFS slide (trang 6):

        function BREADTH-FIRST-SEARCH(problem)
            node <- STATE = start, PATH-COST = 0
            if GOAL-TEST(node.STATE) then return SOLUTION(node)
            frontier <- FIFO queue voi node
            explored <- empty set
            loop do
                if EMPTY?(frontier) then return failure
                node <- POP(frontier)
                add node.STATE to explored
                for each action in ACTIONS(node.STATE) do
                    child <- CHILD-NODE
                    if child.STATE not in explored or frontier then
                        if GOAL-TEST then return SOLUTION
                        frontier <- INSERT(child, frontier)

        Returns:
            list of action names, vd ["North", "East", ...]
            hoac None neu khong tim duoc
        """
        if start == end:
            return []

        # node <- STATE = start
        # frontier <- FIFO queue
        frontier = deque([(start, [])])
        # explored <- empty set
        explored = {start}

        # loop do
        while frontier:
            # if EMPTY?(frontier) then return failure — handled by while

            # node <- POP(frontier)
            current_pos, path = frontier.popleft()

            # for each action in ACTIONS(node.STATE) do
            for action_name, (dr, dc) in DIRECTIONS.items():
                # child <- CHILD-NODE
                next_pos = (current_pos[0] + dr, current_pos[1] + dc)

                # if child.STATE is not in explored or frontier
                if (next_pos not in explored
                        and next_pos not in walls
                        and next_pos not in avoid):

                    new_path = path + [action_name]

                    # if GOAL-TEST(child.STATE) then return SOLUTION
                    if next_pos == end:
                        return new_path

                    # add to explored, INSERT(child, frontier)
                    explored.add(next_pos)
                    frontier.append((next_pos, new_path))

        # return failure
        return None

    # ========================================================
    # BFS TINH KHOANG CACH
    # ========================================================
    def _bfs_distance(self, start, end, walls, avoid):
        """Tinh khoang cach BFS tu start den end."""
        if start == end:
            return 0

        queue = deque([(start, 0)])
        visited = {start}

        while queue:
            pos, dist = queue.popleft()

            r, c = pos
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                neighbor = (r + dr, c + dc)
                if neighbor == end:
                    return dist + 1
                if (neighbor not in visited
                        and neighbor not in walls
                        and neighbor not in avoid):
                    visited.add(neighbor)
                    queue.append((neighbor, dist + 1))

        return float('inf')

    # ========================================================
    # DI CHUYEN VE PHIA MUC TIEU (FALLBACK)
    # ========================================================
    def _move_toward(self, my_pos, target, walls, obstacles):
        """
        Chon huong di gan target nhat (greedy).
        Dung lam fallback khi BFS khong tim duoc duong.
        """
        best_action = "Stay"
        best_dist = float('inf')
        r, c = my_pos

        for action_name, (dr, dc) in DIRECTIONS.items():
            next_pos = (r + dr, c + dc)
            if next_pos not in obstacles:
                dist = abs(next_pos[0] - target[0]) + abs(next_pos[1] - target[1])
                if dist < best_dist:
                    best_dist = dist
                    best_action = action_name

        return best_action


# ============================================================
# ALPHA-BETA PRUNING (NANG CAO - TUY CHON)
# Anh xa tu ma gia slide trang 24
# ============================================================

def alpha_beta_search(game_state, agent, max_depth=2):
    """
    Alpha-Beta Search theo dung ma gia slide (trang 24).

    function ALPHA-BETA-SEARCH(state) returns an action
        v <- MAX-VALUE(state, -inf, +inf)
        return the action in ACTIONS(state) with value v

    Dung cho quyet dinh nang cao hon GBFS.
    max_depth nho (2-3) de dam bao < 1000ms.

    Args:
        game_state: dict trang thai game
        agent: doi tuong Agent
        max_depth: do sau toi da (mac dinh 2)

    Returns:
        string: action name
    """
    walls = game_state["walls"]
    goals = game_state["goals"]
    boxes = game_state["boxes"]
    my_pos = game_state["my_pos"]
    opp_pos = game_state["opponent_pos"]

    best_action = "Stay"
    # v <- -inf
    best_value = float('-inf')
    # alpha, beta
    alpha = float('-inf')
    beta = float('+inf')

    # for each action in ACTIONS(state) do
    for action_name, (dr, dc) in DIRECTIONS.items():
        next_pos = (my_pos[0] + dr, my_pos[1] + dc)

        # Kiem tra hanh dong hop le
        if next_pos in walls or next_pos == opp_pos:
            continue

        # Tao trang thai moi sau khi di chuyen
        new_boxes = set(boxes)
        if next_pos in boxes:
            box_next = (next_pos[0] + dr, next_pos[1] + dc)
            if box_next in walls or box_next in boxes:
                continue
            new_boxes.remove(next_pos)
            new_boxes.add(box_next)

        new_state = {
            "my_pos": next_pos,
            "opponent_pos": opp_pos,
            "boxes": frozenset(new_boxes),
            "goals": goals,
            "walls": walls,
        }

        # v <- MAX(v, MIN-VALUE(RESULT(s,a), alpha, beta))
        v = _min_value(new_state, alpha, beta, max_depth - 1, goals)
        if v > best_value:
            best_value = v
            best_action = action_name

        # if v >= beta then return v (pruning)
        if best_value >= beta:
            return best_action

        # alpha <- MAX(alpha, v)
        alpha = max(alpha, best_value)

    return best_action


def _max_value(state, alpha, beta, depth, goals):
    """
    MAX-VALUE theo ma gia slide (trang 24).

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
        return _utility(state, goals)

    walls = state["walls"]
    my_pos = state["my_pos"]
    opp_pos = state["opponent_pos"]
    boxes = state["boxes"]

    # v <- -inf
    v = float('-inf')

    # for each a in ACTIONS(state) do
    for _, (dr, dc) in DIRECTIONS.items():
        next_pos = (my_pos[0] + dr, my_pos[1] + dc)
        if next_pos in walls or next_pos == opp_pos:
            continue

        new_boxes = set(boxes)
        if next_pos in boxes:
            box_next = (next_pos[0] + dr, next_pos[1] + dc)
            if box_next in walls or box_next in boxes:
                continue
            new_boxes.remove(next_pos)
            new_boxes.add(box_next)

        new_state = {
            "my_pos": next_pos,
            "opponent_pos": opp_pos,
            "boxes": frozenset(new_boxes),
            "goals": goals,
            "walls": walls,
        }

        # v <- MAX(v, MIN-VALUE(RESULT(s,a), alpha, beta))
        v = max(v, _min_value(new_state, alpha, beta, depth - 1, goals))

        # if v >= beta then return v (cat tia beta)
        if v >= beta:
            return v

        # alpha <- MAX(alpha, v)
        alpha = max(alpha, v)

    if v == float('-inf'):
        return _utility(state, goals)

    # return v
    return v


def _min_value(state, alpha, beta, depth, goals):
    """
    MIN-VALUE theo ma gia slide (trang 24).

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
        return _utility(state, goals)

    walls = state["walls"]
    my_pos = state["my_pos"]
    opp_pos = state["opponent_pos"]
    boxes = state["boxes"]

    # v <- +inf
    v = float('+inf')

    # Luot cua doi thu (MIN player)
    # for each a in ACTIONS(state) do
    for _, (dr, dc) in DIRECTIONS.items():
        next_opp = (opp_pos[0] + dr, opp_pos[1] + dc)
        if next_opp in walls or next_opp == my_pos:
            continue

        new_boxes = set(boxes)
        if next_opp in boxes:
            box_next = (next_opp[0] + dr, next_opp[1] + dc)
            if box_next in walls or box_next in boxes:
                continue
            new_boxes.remove(next_opp)
            new_boxes.add(box_next)

        new_state = {
            "my_pos": my_pos,
            "opponent_pos": next_opp,
            "boxes": frozenset(new_boxes),
            "goals": goals,
            "walls": walls,
        }

        # v <- MIN(v, MAX-VALUE(RESULT(s,a), alpha, beta))
        v = min(v, _max_value(new_state, alpha, beta, depth - 1, goals))

        # if v <= alpha then return v (cat tia alpha)
        if v <= alpha:
            return v

        # beta <- MIN(beta, v)
        beta = min(beta, v)

    if v == float('+inf'):
        return _utility(state, goals)

    # return v
    return v


def _utility(state, goals):
    """
    Ham tinh diem (UTILITY) cho trang thai.
    UTILITY = so box cua minh tren goal - so box cua doi thu tren goal.
    Giu don gian: dem box tren goal va uoc tinh.
    """
    boxes = state["boxes"]
    my_pos = state["my_pos"]

    # So box dang o tren goal
    boxes_on_goal = sum(1 for b in boxes if b in goals)

    # Bonus: agent gan goal trong -> tot hon
    min_dist_to_free_goal = float('inf')
    for g in goals:
        if g not in boxes:
            dist = abs(my_pos[0] - g[0]) + abs(my_pos[1] - g[1])
            if dist < min_dist_to_free_goal:
                min_dist_to_free_goal = dist

    # Utility = boxes da vao dich (x10) - khoang cach den goal gan nhat
    score = boxes_on_goal * 10
    if min_dist_to_free_goal < float('inf'):
        score -= min_dist_to_free_goal

    return score
