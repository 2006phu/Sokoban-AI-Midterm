# state.py
# Thanh vien A phu trach
# Class quan ly trang thai game Sokoban


class State:
    """
    Dai dien cho 1 trang thai trong game Sokoban.

    Mot trang thai gom:
        - Vi tri cua agent (tuple)
        - Vi tri cua tat ca boxes (frozenset cua tuples)

    Tai sao dung frozenset?
        - frozenset la immutable (khong thay doi duoc)
        - frozenset la hashable -> dung duoc trong set() va dict()
        - Can thiet de kiem tra state da xet chua (EXPLORED set)

    Tuong ung voi khai niem node.STATE trong ma gia slide.

    Attributes:
        agent_pos:  tuple (row, col) vi tri agent
        boxes:      frozenset cua cac tuple (row, col) vi tri boxes
    """

    def __init__(self, agent_pos, boxes):
        """
        Khoi tao trang thai.

        Args:
            agent_pos: tuple (row, col)
            boxes: co the la set, list, hoac frozenset -> chuyen thanh frozenset
        """
        self.agent_pos = agent_pos
        self.boxes = frozenset(boxes) if not isinstance(boxes, frozenset) else boxes

    def is_goal(self, goals):
        """
        Kiem tra trang thai hien tai co phai goal state khong.

        Tuong ung: problem.GOAL-TEST(node.STATE) trong ma gia.
        Goal state: TAT CA cac vi tri goal deu co box dung tren.

        Args:
            goals: set cac vi tri goal

        Returns:
            True neu tat ca goals deu co box
        """
        return goals.issubset(self.boxes)

    def get_successors(self, game_map):
        """
        Sinh ra tat ca trang thai ke (successor states).

        Tuong ung: problem.ACTIONS(node.STATE) + CHILD-NODE trong ma gia.

        Logic:
        Voi moi huong (North, South, East, West):
            1. Tinh vi tri moi cua agent (next_pos)
            2. Neu next_pos la tuong -> bo qua
            3. Neu next_pos co box:
               a. Tinh vi tri phia sau box (box_next_pos) theo cung huong
               b. Neu box_next_pos la tuong hoac co box khac -> bo qua
               c. Neu box_next_pos trong -> tao state moi (agent o next_pos, box di chuyen)
            4. Neu next_pos trong -> tao state moi (agent o next_pos, boxes giu nguyen)

        Returns:
            list of (action_name, new_state, cost)
            vd: [("North", State(...), 1), ("East", State(...), 1), ...]
        """
        successors = []
        directions = {
            "North": (-1, 0),
            "South": (1, 0),
            "East": (0, 1),
            "West": (0, -1)
        }

        ar, ac = self.agent_pos

        for action, (dr, dc) in directions.items():
            nr, nc = ar + dr, ac + dc
            next_pos = (nr, nc)

            # Kiem tra o ke tiep co hop le va khong phai tuong khong
            if not game_map.is_free(next_pos):
                continue

            if next_pos in self.boxes:
                # Co box phia truoc -> kiem tra o sau box
                box_nr, box_nc = nr + dr, nc + dc
                box_next = (box_nr, box_nc)

                if not game_map.is_free(box_next) or box_next in self.boxes:
                    continue    # Khong the day box ra ngoai ban do hoac vao o bi chan

                # Day box: box di chuyen, agent vao cho box cu
                new_boxes = (self.boxes - {next_pos}) | {box_next}
                new_state = State(next_pos, new_boxes)
                successors.append((action, new_state, 1))

            else:
                # O trong: agent di chuyen binh thuong
                new_state = State(next_pos, self.boxes)
                successors.append((action, new_state, 1))

        return successors

    def __eq__(self, other):
        """Hai state bang nhau khi agent_pos va boxes giong nhau."""
        if not isinstance(other, State):
            return False
        return self.agent_pos == other.agent_pos and self.boxes == other.boxes

    def __hash__(self):
        """
        Hash cua state de dung trong set va dict.
        Can thiet cho explored set trong UCS/A*.
        """
        return hash((self.agent_pos, self.boxes))

    def __lt__(self, other):
        """De so sanh trong priority queue khi 2 state co cung f(n)."""
        return self.agent_pos < other.agent_pos

    def __repr__(self):
        return f"State(agent={self.agent_pos}, boxes={set(self.boxes)})"
