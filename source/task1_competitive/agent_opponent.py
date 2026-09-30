# agent_opponent.py
# Thuoc ve nhom doi thu / Agent 2 (Req 8)
#
# FILE NAY TACH BIET HOAN TOAN VOI agent_algorithm.py de thi dau giua 2 nhom.
# Thuat toan: Greedy Search ket hop BFS pathfinding

from collections import deque
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
    Agent doi thu (Agent 2) thi dau trong che do competitive.
    Chien luoc: Greedy Target Locking + BFS Pathfinding
    """

    def __init__(self, agent_id=2):
        self.agent_id = agent_id

    def choose_action(self, game_state):
        """
        Ra quyet dinh trong vong toi da 1000ms.
        """
        start_time = time.time()
        my_pos = game_state["my_pos"]
        opp_pos = game_state["opponent_pos"]
        walls = game_state["walls"]
        boxes = game_state["boxes"]
        goals = game_state["goals"]

        # Tim goal trong gan nhat
        best_goal = None
        best_goal_dist = float('inf')
        for g in goals:
            if g not in boxes:
                d = abs(my_pos[0] - g[0]) + abs(my_pos[1] - g[1])
                if d < best_goal_dist:
                    best_goal_dist = d
                    best_goal = g

        if not best_goal:
            # Neu tat ca goal deu co hop -> co the thu day hop cua doi thu ra ngoai
            return "Stay"

        # Tim hop gan nhat co the day ve goal
        best_box = None
        best_box_dist = float('inf')
        for b in boxes:
            d = abs(my_pos[0] - b[0]) + abs(my_pos[1] - b[1])
            if d < best_box_dist:
                best_box_dist = d
                best_box = b

        if not best_box:
            return "Stay"

        # Tim vi tri day (dung sau lung hop theo huong day ve goal)
        dr = best_goal[0] - best_box[0]
        dc = best_goal[1] - best_box[1]
        step_r = (dr // abs(dr)) if dr != 0 else 0
        step_c = (dc // abs(dc)) if dc != 0 else 0

        # Thu huong uu tien
        push_pos = (best_box[0] - step_r, best_box[1] - step_c)
        target_cell = (best_box[0] + step_r, best_box[1] + step_c)

        if my_pos == push_pos and target_cell not in walls and target_cell not in boxes and target_cell != opp_pos:
            return direction_name(step_r, step_c)

        # BFS tim duong den vi tri day
        avoid = boxes | {opp_pos}
        path = self._bfs(my_pos, push_pos, walls, avoid)

        # Dam bao luon tra ve trong 1000ms
        if time.time() - start_time > 0.9:
            return "Stay"

        if path and len(path) > 0:
            return path[0]

        # Fallback: buoc vao o trong bat ky gan goal hon
        for act, (d_r, d_c) in DIRECTIONS.items():
            nxt = (my_pos[0] + d_r, my_pos[1] + d_c)
            if nxt not in walls and nxt not in boxes and nxt != opp_pos:
                return act

        return "Stay"

    def _bfs(self, start, target, walls, avoid):
        if start == target:
            return []
        queue = deque([(start, [])])
        visited = {start}

        while queue:
            curr, path = queue.popleft()
            for name, (dr, dc) in DIRECTIONS.items():
                nxt = (curr[0] + dr, curr[1] + dc)
                if nxt not in visited and nxt not in walls and (nxt not in avoid or nxt == target):
                    new_path = path + [name]
                    if nxt == target:
                        return new_path
                    visited.add(nxt)
                    queue.append((nxt, new_path))
        return None
