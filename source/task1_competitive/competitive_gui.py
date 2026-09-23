# competitive_gui.py
# Thanh vien C phu trach (Req 8)
# GUI cho che do thi dau 2 agent

import pygame
import sys

# Mau sac cho 2 agent
COLOR_AGENT_1 = (30, 144, 255)     # Xanh duong
COLOR_AGENT_2 = (255, 69, 0)       # Do cam
COLOR_BOX_AGENT_1 = (100, 149, 237)  # Xanh nhat (box cua agent 1)
COLOR_BOX_AGENT_2 = (255, 140, 0)   # Cam (box cua agent 2)
COLOR_BOX_NEUTRAL = (210, 105, 30)   # Nau (box chua ai dat)
COLOR_WALL = (139, 119, 101)
COLOR_FLOOR = (245, 222, 179)
COLOR_GOAL = (255, 105, 180)
COLOR_TEXT = (255, 255, 255)

CELL_SIZE = 60
FPS = 60


class CompetitiveGUI:
    """
    Giao dien game Sokoban che do thi dau 2 agent.

    Khac biet so voi GUI single-player:
    1. Hien thi 2 agent voi mau khac nhau
    2. Box cua moi agent co mau rieng
    3. Hien thi diem so cua tung agent
    4. Hien thi so buoc con lai
    5. User nhap so buoc n truoc khi bat dau

    Mo rong tu gui.py cua task1.
    """

    def __init__(self, game_map):
        """
        Khoi tao GUI thi dau.

        Goi y:
        - Lay so buoc n tu user: n = int(input("Nhap so buoc thi dau: "))
        - Khoi tao 2 agent tu agent_algorithm.py
        - pygame.init()
        """
        # TODO: Khoi tao
        pass

    def run(self):
        """
        Vong lap chinh.

        Moi buoc:
        1. Ca 2 agent chon action (dong thoi)
        2. Kiem tra xung dot
        3. Thuc hien actions hop le
        4. Cap nhat diem so
        5. Ve man hinh
        6. Kiem tra het n buoc -> thong bao nguoi thang

        Goi y xu ly dong thoi:
        - Goi agent1.choose_action() va agent2.choose_action()
        - Kiem tra: neu 2 agent muon vao cung o -> ca 2 dung yen
        - Kiem tra: neu 2 agent di xuyen qua nhau -> ca 2 dung yen
        """
        # TODO: Implement game loop
        pass

    def resolve_conflicts(self, action1, action2, state):
        """
        Giai quyet xung dot khi 2 agent hanh dong dong thoi.

        Cac truong hop xung dot:
        1. Ca 2 muon vao CUNG O -> ca 2 dung yen
        2. Ca 2 day CUNG BOX -> ca 2 dung yen (hoac uu tien)
        3. Agent 1 di vao o cua Agent 2 va nguoc lai (swap) -> ca 2 dung yen

        Returns:
            (resolved_action1, resolved_action2)
        """
        # TODO: Implement
        pass

    def update_scores(self, state):
        """
        Cap nhat diem so: dem so box cua moi agent dang o vi tri goal.

        Luu y: 1 box co the bi doi thu day ra khoi goal
        -> diem giam
        """
        # TODO: Implement
        pass

    def draw(self, state):
        """
        Ve man hinh thi dau.

        Can hien thi:
        1. Ban do (tuong, san, goal)
        2. Agent 1 (mau xanh) va Agent 2 (mau do)
        3. Box cua agent 1 (mau xanh nhat) va box cua agent 2 (mau cam)
        4. Box chua ai dat (mau nau)
        5. Panel: diem agent 1, diem agent 2, buoc con lai
        """
        # TODO: Implement
        pass

    def show_result(self, score1, score2):
        """
        Hien thi ket qua khi het n buoc.

        - Agent 1 thang / Agent 2 thang / Hoa
        - Diem so chi tiet
        """
        # TODO: Implement
        pass


if __name__ == "__main__":
    # TODO:
    # from game_map import GameMap
    # game_map = GameMap("maps/competitive_map.txt")
    # gui = CompetitiveGUI(game_map)
    # gui.run()
    pass
