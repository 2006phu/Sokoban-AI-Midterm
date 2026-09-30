# game_map.py cho task1_competitive
# Quan ly ban do thi dau 2 agent

from collections import deque


class CompetitiveGameMap:
    """
    Doc va quan ly ban do cho che do thi dau 2 agent.

    Ky hieu:
        '%' = Tuong
        '1' hoac 'A' = Agent 1
        '2' hoac 'E' = Agent 2
        'B' = Hop (Box)
        'D' = Vi tri dich (Designated goal)
        'C' = Hop dang tren dich
        ' ' = O trong (Floor)
    """

    def __init__(self, file_path):
        self.walls = set()
        self.goals = set()
        self.boxes = set()
        self.agent1_pos = None
        self.agent2_pos = None
        self.rows = 0
        self.cols = 0
        self.floor_cells = set()

        self._load(file_path)
        self._compute_floor()

    def _load(self, file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        self.rows = len(lines)
        self.cols = 0

        for r, line in enumerate(lines):
            line = line.rstrip("\r\n")
            if len(line) > self.cols:
                self.cols = len(line)

            for c, ch in enumerate(line):
                pos = (r, c)
                if ch == "%":
                    self.walls.add(pos)
                elif ch in ("1", "A"):
                    self.agent1_pos = pos
                elif ch in ("2", "E"):
                    self.agent2_pos = pos
                elif ch == "B":
                    self.boxes.add(pos)
                elif ch == "D":
                    self.goals.add(pos)
                elif ch == "C":
                    self.boxes.add(pos)
                    self.goals.add(pos)

    def _compute_floor(self):
        """BFS flood fill tim cac o san ben trong tuong."""
        start_nodes = []
        if self.agent1_pos:
            start_nodes.append(self.agent1_pos)
        if self.agent2_pos:
            start_nodes.append(self.agent2_pos)

        visited = set(start_nodes)
        queue = deque(start_nodes)

        while queue:
            r, c = queue.popleft()
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nr, nc = r + dr, c + dc
                npos = (nr, nc)
                if (0 <= nr < self.rows and 0 <= nc < self.cols
                        and npos not in self.walls
                        and npos not in visited):
                    visited.add(npos)
                    queue.append(npos)

        self.floor_cells = visited

    def is_wall(self, position):
        return position in self.walls

    def is_free(self, position):
        r, c = position
        return (0 <= r < self.rows
                and 0 <= c < self.cols
                and position not in self.walls)

    def get_neighbors(self, position):
        r, c = position
        neighbors = []
        for name, (dr, dc) in [("North", (-1, 0)), ("South", (1, 0)),
                               ("East", (0, 1)), ("West", (0, -1))]:
            nr, nc = r + dr, c + dc
            if self.is_free((nr, nc)):
                neighbors.append((name, (nr, nc)))
        return neighbors
