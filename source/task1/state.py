# state.py
# Quan ly trang thai (State) cua game Sokoban


class State:
    """
    Bieu dien mot trang thai cua game Sokoban:
    - agent_pos: (row, col) vi tri agent
    - boxes: frozenset cac vi tri hop (hashable de luu trong set explored)
    """

    def __init__(self, agent_pos, boxes):
        self.agent_pos = agent_pos
        self.boxes = frozenset(boxes) if not isinstance(boxes, frozenset) else boxes

    def is_goal(self, goals):
        """Kiem tra tat ca vi tri goal deu co box."""
        return goals.issubset(self.boxes)

    def get_successors(self, game_map):
        """
        Sinh danh sach trang thai ke tiep hop le.
        Returns:
            list of (action_name, new_state, cost)
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
