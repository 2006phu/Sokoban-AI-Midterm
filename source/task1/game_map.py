# game_map.py
# Thanh vien A phu trach
# Class quan ly ban do Sokoban

class GameMap:
    """
    Doc va quan ly ban do Sokoban tu file text.

    Ky hieu trong file ban do:
        '%' = tuong (wall)
        'A' = vi tri ban dau cua agent
        'B' = hop (box)
        'D' = vi tri dich (goal/designated position)
        'C' = hop dang o vi tri dich (box on goal)
        ' ' = o trong (blank cell)

    Attributes:
        walls:      set cac toa do tuong         vd: {(0,0), (0,1), ...}
        goals:      set cac toa do dich          vd: {(2,1), (4,1), ...}
        agent_pos:  tuple vi tri agent ban dau   vd: (2, 2)
        boxes:      set vi tri cac box ban dau   vd: {(2,3), (3,4), ...}
        rows:       so hang cua ban do
        cols:       so cot cua ban do (lay hang dai nhat)
    """

    def __init__(self, file_path):
        """
        Doc file ban do va khoi tao cac thuoc tinh.

        Goi y:
        - Doc file theo tung dong
        - Duyet tung ky tu, xac dinh toa do (hang, cot)
        - Phan loai ky tu vao walls, goals, boxes, agent_pos
        - Luu y: 'C' = box + goal (them ca vao boxes va goals)
        """
        self.walls = set()
        self.goals = set()
        self.boxes = set()
        self.agent_pos = None
        self.rows = 0
        self.cols = 0

        # TODO: Doc file va parse ban do
        # Buoc 1: Mo file, doc tung dong
        # Buoc 2: Duyet tung ky tu trong dong
        # Buoc 3: Dua vao ky tu, them toa do vao set tuong ung
        # Buoc 4: Tinh rows va cols

    def is_wall(self, position):
        """Kiem tra vi tri co phai tuong khong."""
        # TODO: return True neu position nam trong self.walls
        pass

    def is_free(self, position):
        """Kiem tra vi tri co trong khong (khong phai tuong)."""
        # TODO: return True neu position KHONG phai tuong
        # va nam trong pham vi ban do
        pass

    def get_neighbors(self, position):
        """
        Tra ve danh sach cac o ke (North, South, East, West).

        Returns:
            list of (direction_name, new_position)
            vd: [("North", (1,2)), ("East", (2,3)), ...]
        """
        # TODO: Tinh 4 vi tri ke
        # North: (row-1, col)
        # South: (row+1, col)
        # East:  (row, col+1)
        # West:  (row, col-1)
        pass

    def print_map(self, agent_pos, boxes):
        """
        In ban do ra console (dung de debug).

        Goi y: Duyet tung o, in ky tu tuong ung
        """
        # TODO: In ban do voi vi tri agent va boxes hien tai
        pass
