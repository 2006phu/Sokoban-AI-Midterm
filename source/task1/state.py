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
        self.boxes = frozenset(boxes)

    def is_goal(self, goals):
        """
        Kiem tra trang thai hien tai co phai goal state khong.

        Goal state: TAT CA cac vi tri goal deu co box dung tren.

        Args:
            goals: set cac vi tri goal

        Returns:
            True neu tat ca goals deu co box

        Goi y: Kiem tra goals.issubset(self.boxes)
        hoac goals la tap con cua self.boxes
        """
        # TODO: Kiem tra moi goal co box khong
        pass

    def get_successors(self, game_map):
        """
        Sinh ra tat ca trang thai ke (successor states).

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

        # TODO: Voi moi huong, kiem tra va tao state moi
        # Buoc 1: Tinh next_pos = (agent_row + dr, agent_col + dc)
        # Buoc 2: Kiem tra next_pos co phai tuong khong
        # Buoc 3: Kiem tra next_pos co box khong
        # Buoc 4: Neu co box, kiem tra o phia sau box
        # Buoc 5: Tao State moi va them vao successors

        return successors

    def __eq__(self, other):
        """Hai state bang nhau khi agent_pos va boxes giong nhau."""
        # TODO: So sanh self va other
        pass

    def __hash__(self):
        """
        Hash cua state de dung trong set va dict.

        Goi y: return hash((self.agent_pos, self.boxes))
        """
        # TODO: Tra ve hash value
        pass

    def __lt__(self, other):
        """
        De so sanh trong priority queue khi 2 state co cung f(n).
        Co the so sanh tuy y, vd theo agent_pos.
        """
        # TODO: return True/False tuy y
        pass
