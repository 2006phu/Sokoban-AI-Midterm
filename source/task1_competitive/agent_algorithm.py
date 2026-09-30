# agent_algorithm.py
# Thanh vien A phu trach thuat toan (Req 7)
# Thanh vien C tich hop vao game (Req 8)
#
# Thuat toan: GBFS (Greedy Best-First Search) ket hop BFS Pathfinding va Target Locking
# Gioi han: Thoi gian ra quyet dinh luon <= 1000ms

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
    Agent 1 (Nhom cua ban) thi dau trong che do competitive.
    Chien luoc:
    - Target Locking de tranh hien tuong doi muc tieu lien tuc gay dao dong (oscillation)
    - Tinh toan vi tri day hop truc giao hop le
    - BFS tim duong toi uu den vi tri day
    """

    def __init__(self, agent_id=1):
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

        # Chi xet cac hop CHUA vao dich va cac dich CHUA co hop
        unplaced_boxes = [b for b in boxes if b not in goals]
        free_goals = [g for g in goals if g not in boxes]

        if not unplaced_boxes or not free_goals:
            # Tat ca hop da vao dich -> co the tim cach day hop doi thu ra ngoai hoac dung yen
            return "Stay"

        # Kiem tra muc tieu hien tai con hop le khong
        if self.target_box not in unplaced_boxes or self.target_goal not in free_goals:
            self.target_box = None
            self.target_goal = None

        # Chon cap (hop, dich) toi uu neu chua co muc tieu
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

        # Tim vi tri day truc giao tot nhat
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
            # Khong day duoc hop nay hien tai -> bo qua chon hop khac o luot sau
            self.target_box = None
            return "Stay"

        push_action_name, agent_pos_req = best_push

        # Neu da dung dung vi tri day -> Thuc hien day hop!
        if my_pos == agent_pos_req:
            return push_action_name

        # BFS tim duong ngan nhat den vi tri day
        avoid = boxes | {opp_pos}
        path = self._bfs_path(my_pos, agent_pos_req, walls, avoid)

        # Dam bao khong vuot qua 1000ms
        if time.time() - start_time > 0.9:
            return "Stay"

        if path and len(path) > 0:
            return path[0]

        # Neu bi chan duong -> reset target de tim duong khac
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
