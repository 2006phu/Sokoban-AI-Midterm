# agent_opponent.py
# Thuoc ve Agent 2 (Doi thu thi dau - Req 8)
#
# Thuat toan: Greedy Best-First Search doc lap voi Chien Luoc Cuop Hop (Req 6)

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
    Bao gom tinh nang day hop va cuop hop cua doi thu.
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
        ownership = game_state.get("box_ownership", {})
        my_id = self.agent_id
        opp_id = 1 if my_id == 2 else 2

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
