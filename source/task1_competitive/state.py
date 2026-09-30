# state.py
# Quan ly trang thai cuoc thi dau 2 agent

MOVE_VECTORS = {
    "North": (-1, 0),
    "South": (1, 0),
    "East":  (0, 1),
    "West":  (0, -1),
    "Stay":  (0, 0),
}


class CompetitiveState:
    """
    Dai dien cho trang thai tro choi thi dau 2 agent.

    Cac thanh phan:
    - pos1: (row, col) vi tri Agent 1
    - pos2: (row, col) vi tri Agent 2
    - boxes: frozenset cac vi tri hop
    - box_ownership: dict {box_pos: agent_id} (1 hoac 2 neu da vao goal)
    - step: buoc hien tai (0 den step_limit)
    - step_limit: gioi han n buoc do user nhap
    """

    def __init__(self, pos1, pos2, boxes, step_limit=50, box_ownership=None, step=0):
        self.pos1 = pos1
        self.pos2 = pos2
        self.boxes = frozenset(boxes)
        self.step_limit = step_limit
        self.step = step
        self.box_ownership = dict(box_ownership) if box_ownership else {}

    def get_score(self, agent_id, goals):
        """
        Diem cua agent = so hop ma agent do da dua vao goal va hien van o tren goal.
        """
        score = 0
        for box_pos, owner in self.box_ownership.items():
            if owner == agent_id and box_pos in goals and box_pos in self.boxes:
                score += 1
        return score

    def is_game_over(self):
        """Kiem tra tro choi da ket thuc chua (het n buoc)."""
        return self.step >= self.step_limit

    def get_winner(self, goals):
        """
        Tra ve:
            1: Agent 1 thang
            2: Agent 2 thang
            0: Hoa (Draw)
        """
        s1 = self.get_score(1, goals)
        s2 = self.get_score(2, goals)
        if s1 > s2:
            return 1
        elif s2 > s1:
            return 2
        return 0

    def resolve_step(self, action1, action2, game_map):
        """
        Thuc hien hanh dong dong thoi cua ca 2 agent va giai quyet xung dot.

        Quy tac giai quyet xung dot:
        1. Hai agent cung di vao mot o -> Ca hai dung yen.
        2. Hai agent di xuyen qua nhau (doi cho nhau) -> Ca hai dung yen.
        3. Day hop:
           - Chi day duoc khi o sau hop trong, khong phai tuong, khong co hop khac,
             va khong bi doi thu can.
           - Neu ca hai agent cung day cung 1 hop -> Hop khong di chuyen.
        4. Cap nhat quyen so huu (box_ownership):
           - Neu hop duoc day vao goal, agent day se chiem quyen so huu hop do.
           - Neu hop bi day ra khoi goal, quyen so huu tren goal do bi huy bo.
        """
        dr1, dc1 = MOVE_VECTORS.get(action1, (0, 0))
        dr2, dc2 = MOVE_VECTORS.get(action2, (0, 0))

        p1 = self.pos1
        p2 = self.pos2
        desired1 = (p1[0] + dr1, p1[1] + dc1)
        desired2 = (p2[0] + dr2, p2[1] + dc2)

        boxes_list = set(self.boxes)
        new_ownership = dict(self.box_ownership)

        # ----------------------------------------------------
        # Buoc 1: Kiem tra hanh dong co hop le voi tuong khong
        # ----------------------------------------------------
        valid1 = game_map.is_free(desired1) if action1 != "Stay" else True
        valid2 = game_map.is_free(desired2) if action2 != "Stay" else True

        if not valid1:
            desired1 = p1
            dr1, dc1 = 0, 0
        if not valid2:
            desired2 = p2
            dr2, dc2 = 0, 0

        # ----------------------------------------------------
        # Buoc 2: Kiem tra tuong tac voi hop (Day hop)
        # ----------------------------------------------------
        push1_box = None
        push1_target = None
        if desired1 in boxes_list and action1 != "Stay":
            push1_target = (desired1[0] + dr1, desired1[1] + dc1)
            # O dich cua hop phai trong
            if (not game_map.is_free(push1_target)
                    or push1_target in boxes_list
                    or push1_target == p2):
                # Khong the day hop -> Agent 1 dung yen
                desired1 = p1
                push1_target = None
            else:
                push1_box = desired1

        push2_box = None
        push2_target = None
        if desired2 in boxes_list and action2 != "Stay":
            push2_target = (desired2[0] + dr2, desired2[1] + dc2)
            if (not game_map.is_free(push2_target)
                    or push2_target in boxes_list
                    or push2_target == p1):
                desired2 = p2
                push2_target = None
            else:
                push2_box = desired2

        # ----------------------------------------------------
        # Buoc 3: Xung dot giua 2 Agent
        # ----------------------------------------------------
        # TH 3.1: Hai agent cung day CUNG MOT HOP
        if push1_box is not None and push1_box == push2_box:
            desired1 = p1
            desired2 = p2
            push1_box = push1_target = None
            push2_box = push2_target = None

        # TH 3.2: Hai agent cung muon buoc vao 1 o
        if desired1 == desired2 and desired1 != p1 and desired2 != p2:
            desired1 = p1
            desired2 = p2
            push1_box = push1_target = None
            push2_box = push2_target = None

        # TH 3.3: Hai agent doi cho nhau (swap head-on)
        if desired1 == p2 and desired2 == p1:
            desired1 = p1
            desired2 = p2
            push1_box = push1_target = None
            push2_box = push2_target = None

        # TH 3.4: Hop cua agent 1 bi day vao vi tri desired cua agent 2
        if push1_target and push1_target == desired2:
            desired2 = p2
        if push2_target and push2_target == desired1:
            desired1 = p1

        # ----------------------------------------------------
        # Buoc 4: Cap nhat vi tri hop va quyen so huu
        # ----------------------------------------------------
        if push1_box and push1_target:
            boxes_list.remove(push1_box)
            boxes_list.add(push1_target)
            old_owner = new_ownership.pop(push1_box, None)
            if push1_target in game_map.goals:
                new_ownership[push1_target] = 1  # Agent 1 chiem hop nay
            elif old_owner is not None and push1_box in game_map.goals:
                pass  # Hop bi day ra khoi goal -> mat diem tren goal cu

        if push2_box and push2_target:
            boxes_list.remove(push2_box)
            boxes_list.add(push2_target)
            old_owner = new_ownership.pop(push2_box, None)
            if push2_target in game_map.goals:
                new_ownership[push2_target] = 2  # Agent 2 chiem hop nay
            elif old_owner is not None and push2_box in game_map.goals:
                pass

        # Tra ve state moi
        return CompetitiveState(
            pos1=desired1,
            pos2=desired2,
            boxes=boxes_list,
            step_limit=self.step_limit,
            box_ownership=new_ownership,
            step=self.step + 1
        )
