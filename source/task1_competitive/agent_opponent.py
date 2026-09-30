# agent_opponent.py
# Thuoc ve Agent 2 (Doi thu thi dau - Req 8)
#
# Thuat toan: Greedy Best-First Search doc lap voi Target Locking

from collections import deque
import time

DIRECTIONS = {
    "North": (-1, 0),
    "South": (1, 0),
    "East":  (0, 1),
    "West":  (0, -1)
}


class Agent:
    """
    Agent 2 (Doi thu) thi dau trong che do competitive.
    Tach biet file de thi dau giua cac nhom (Req 8).
    """

    def __init__(self, agent_id=2):
        self.agent_id = agent_id
        self.target_box = None
        self.target_goal = None

    def choose_action(self, game_state):
        start_time = time.time()
        my_pos = game_state["my_pos"]
        opp_pos = game_state["opponent_pos"]
        walls = game_state["walls"]
        boxes = game_state["boxes"]
        goals = game_state["goals"]

        # Chi xet hop chua dat va goal chua bi chiem
        unplaced_boxes = [b for b in boxes if b not in goals]
        free_goals = [g for g in goals if g not in boxes]

        if not unplaced_boxes or not free_goals:
            return "Stay"

        # Kiem tra muc tieu hien tai
        if self.target_box not in unplaced_boxes or self.target_goal not in free_goals:
            self.target_box = None
            self.target_goal = None

        # Chon muc tieu tot nhat
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

        if self.target_box is None:
            return "Stay"

        tb = self.target_box
        tg = self.target_goal

        # Tim huong day hop hop le
        best_push = None
        best_push_dist = float('inf')

        for name, (dr, dc) in DIRECTIONS.items():
            box_dest = (tb[0] + dr, tb[1] + dc)
            agent_req = (tb[0] - dr, tb[1] - dc)

            if (box_dest not in walls and box_dest not in boxes and box_dest != opp_pos
                    and agent_req not in walls and agent_req not in boxes and agent_req != opp_pos):
                d = abs(box_dest[0] - tg[0]) + abs(box_dest[1] - tg[1])
                if d < best_push_dist:
                    best_push_dist = d
                    best_push = (name, agent_req)

        if not best_push:
            self.target_box = None
            return "Stay"

        push_action_name, agent_pos_req = best_push

        if my_pos == agent_pos_req:
            return push_action_name

        avoid = boxes | {opp_pos}
        path = self._bfs_path(my_pos, agent_pos_req, walls, avoid)

        if time.time() - start_time > 0.9:
            return "Stay"

        if path and len(path) > 0:
            return path[0]

        self.target_box = None
        return "Stay"

    def _bfs_path(self, start, target, walls, avoid):
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
