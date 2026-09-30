# game_map.py
# Thanh vien A phu trach
# Class quan ly ban do Sokoban

from collections import deque


class GameMap:
    """
    Doc va quan ly ban do Sokoban tu file text.

    Ky hieu trong file ban do:
        '%' = tuong (wall)
        'A' = vi tri ban dau cua agent (the man)
        'B' = hop (box)
        'D' = vi tri dich (goal/designated position)
        'C' = hop dang o vi tri dich (box on goal)
        ' ' = o trong (blank cell)

    Attributes:
        walls:       set cac toa do tuong         vd: {(0,0), (0,1), ...}
        goals:       set cac toa do dich          vd: {(2,1), (4,1), ...}
        agent_pos:   tuple vi tri agent ban dau   vd: (2, 2)
        boxes:       set vi tri cac box ban dau   vd: {(2,3), (3,4), ...}
        rows:        so hang cua ban do
        cols:        so cot cua ban do (lay hang dai nhat)
        floor_cells: set cac o thuoc vung choi (ben trong tuong)
    """

    def __init__(self, file_path):
        """
        Doc file ban do va khoi tao cac thuoc tinh.

        Buoc 1: Mo file, doc tung dong
        Buoc 2: Duyet tung ky tu, xac dinh toa do (hang, cot)
        Buoc 3: Phan loai ky tu vao walls, goals, boxes, agent_pos
        Buoc 4: Tinh rows, cols
        Buoc 5: BFS flood-fill tim vung san (floor_cells)
        """
        self.walls = set()
        self.goals = set()
        self.boxes = set()
        self.agent_pos = None
        self.rows = 0
        self.cols = 0
        self.floor_cells = set()

        self._load(file_path)
        self._compute_floor()

    def _load(self, file_path):
        """Doc file ban do va parse thanh cac thanh phan."""
        with open(file_path, "r") as f:
            lines = f.readlines()

        self.rows = len(lines)
        self.cols = 0

        for row, line in enumerate(lines):
            line = line.rstrip("\n").rstrip("\r")
            if len(line) > self.cols:
                self.cols = len(line)

            for col, ch in enumerate(line):
                pos = (row, col)

                if ch == "%":
                    self.walls.add(pos)

                elif ch == "A":
                    self.agent_pos = pos

                elif ch == "B":
                    self.boxes.add(pos)

                elif ch == "D":
                    self.goals.add(pos)

                elif ch == "C":
                    # Box dang o tren goal
                    self.boxes.add(pos)
                    self.goals.add(pos)
                # ' ' (space) = o trong, khong can luu

    def _compute_floor(self):
        """
        Tim tat ca o thuoc vung choi (ben trong tuong).
        Dung BFS tu vi tri agent de xac dinh cac o co the di den.

        Thuat toan BFS (theo slide trang 6):
        - frontier = FIFO queue (deque)
        - explored = empty set
        - Loang ra 4 huong, chi di vao o khong phai tuong
        """
        if self.agent_pos is None:
            return

        visited = set()
        queue = deque([self.agent_pos])
        visited.add(self.agent_pos)

        while queue:
            pos = queue.popleft()
            r, c = pos
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
        """Kiem tra vi tri co phai tuong khong."""
        return position in self.walls

    def is_free(self, position):
        """Kiem tra vi tri co trong khong (khong phai tuong, trong pham vi ban do)."""
        r, c = position
        return (0 <= r < self.rows
                and 0 <= c < self.cols
                and position not in self.walls)

    def get_neighbors(self, position):
        """
        Tra ve danh sach cac o ke co the di den (khong co tuong).

        Returns:
            list of (direction_name, new_position)
            vd: [("North", (1,2)), ("East", (2,3)), ...]
        """
        r, c = position
        neighbors = []
        for name, (dr, dc) in [("North", (-1, 0)), ("South", (1, 0)),
                                ("East", (0, 1)), ("West", (0, -1))]:
            nr, nc = r + dr, c + dc
            if self.is_free((nr, nc)):
                neighbors.append((name, (nr, nc)))
        return neighbors

    def print_map(self, agent_pos, boxes):
        """In ban do ra console (dung de debug)."""
        for r in range(self.rows):
            row_str = ""
            for c in range(self.cols):
                pos = (r, c)
                if pos == agent_pos:
                    row_str += "A"
                elif pos in boxes and pos in self.goals:
                    row_str += "C"
                elif pos in boxes:
                    row_str += "B"
                elif pos in self.goals:
                    row_str += "D"
                elif pos in self.walls:
                    row_str += "%"
                elif pos in self.floor_cells:
                    row_str += " "
                else:
                    row_str += " "
            print(row_str)
