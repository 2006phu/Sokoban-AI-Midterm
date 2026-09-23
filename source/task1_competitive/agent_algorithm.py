# agent_algorithm.py
# Thanh vien A phu trach thuat toan (Req 7)
# Thanh vien C tich hop vao game (Req 8)
#
# FILE NAY PHAI TACH RIENG de cac nhom co the thi dau voi nhau
# Moi nhom viet 1 agent_algorithm.py rieng

from collections import deque


class Agent:
    """
    Agent thi dau trong che do competitive.

    Moi agent can:
    1. Biet vi tri hien tai cua minh
    2. Biet vi tri doi thu
    3. Chon hanh dong trong gioi han 1000ms

    Attributes:
        agent_id:   0 hoac 1 (phan biet 2 agent)
        position:   tuple (row, col) vi tri hien tai
    """

    def __init__(self, agent_id):
        self.agent_id = agent_id
        self.position = None

    def choose_action(self, game_state):
        """
        Chon hanh dong tiep theo.

        GIOI HAN: Phai tra ve trong 1000ms

        Args:
            game_state: dict chua thong tin hien tai
                {
                    "my_pos": (row, col),
                    "opponent_pos": (row, col),
                    "boxes": set of (row, col),
                    "my_boxes_on_goal": int,       # so box minh da dat
                    "opponent_boxes_on_goal": int,  # so box doi thu da dat
                    "goals": set of (row, col),
                    "walls": set of (row, col),
                    "steps_remaining": int,         # so buoc con lai
                }

        Returns:
            string: "North", "South", "East", "West", hoac "Stay"

        Chien luoc goi y:
        1. Tim goal gan nhat chua co box
        2. Tim box gan nhat co the day den goal do
        3. Dung BFS/A* tim duong tu agent den vi tri day box
        4. Tra ve buoc tiep theo tren duong di
        5. Neu doi thu chan duong -> tim duong thay the
        """
        # TODO: Implement chien luoc agent
        # Buoc 1: Phan tich tinh hinh (goals trong, box gan, doi thu)
        # Buoc 2: Chon muc tieu (goal + box)
        # Buoc 3: Tim duong di
        # Buoc 4: Tra ve hanh dong
        return "Stay"

    def find_nearest_free_goal(self, game_state):
        """
        Tim goal gan nhat chua co box (hoac co box cua doi thu).

        Returns:
            tuple (row, col) hoac None
        """
        # TODO: Implement
        pass

    def find_nearest_box(self, game_state, target_goal):
        """
        Tim box gan nhat co the day den target_goal.

        Returns:
            tuple (row, col) hoac None
        """
        # TODO: Implement
        pass

    def find_push_position(self, box_pos, target_goal, game_state):
        """
        Tim vi tri agent can dung de day box ve phia goal.

        Goi y:
        - Xac dinh huong day (tu box den goal)
        - Vi tri day = phia doi dien cua huong day
        - Kiem tra vi tri day co trong khong

        Returns:
            tuple (row, col) vi tri agent can dung de day box
        """
        # TODO: Implement
        pass

    def bfs_path(self, start, end, game_state):
        """
        Tim duong ngan nhat tu start den end, tranh tuong, box, va doi thu.

        Returns:
            list of actions, vd ["North", "East", ...]
            hoac None neu khong tim duoc
        """
        # TODO: Implement BFS tim duong
        pass
