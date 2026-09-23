# gui.py
# Thanh vien A phu trach
# Giao dien game Sokoban bang pygame

import pygame
import sys

# Mau sac goi y (co the thay doi)
COLOR_WALL = (139, 119, 101)     # Nau dam
COLOR_FLOOR = (245, 222, 179)    # Vang nhat
COLOR_BOX = (210, 105, 30)       # Cam
COLOR_BOX_ON_GOAL = (139, 69, 19)  # Nau dam hon
COLOR_GOAL = (255, 105, 180)     # Hong
COLOR_AGENT = (30, 144, 255)     # Xanh duong
COLOR_BG = (50, 50, 50)         # Nen xam dam
COLOR_TEXT = (255, 255, 255)     # Trang

# Kich thuoc
CELL_SIZE = 60                   # Pixel moi o
FPS = 60                         # Frame per second


class GameGUI:
    """
    Giao dien game Sokoban dung pygame.

    Chuc nang yeu cau:
    1. Chon thuat toan: UCS hoac A*
    2. Hien thi so buoc (number of actions) tren UI
    3. Space: pause/resume
    4. -> (Right): tien 1 buoc
    5. <- (Left): lui 1 buoc

    Attributes:
        game_map:   doi tuong GameMap
        solution:   list cac actions (ket qua tu solver)
        states:     list cac state tuong ung voi moi buoc
        current_step: buoc hien tai dang hien thi
        paused:     True/False trang thai pause
        screen:     pygame display surface
    """

    def __init__(self, game_map, solution_actions, solution_states):
        """
        Khoi tao GUI.

        Args:
            game_map: doi tuong GameMap
            solution_actions: list actions, vd ["North", "East", ...]
            solution_states: list states tuong ung voi moi buoc
                            (bao gom state ban dau)

        Goi y:
        - Tinh kich thuoc cua so: cols * CELL_SIZE x rows * CELL_SIZE + panel
        - pygame.init()
        - pygame.display.set_mode((width, height))
        - pygame.display.set_caption("Sokoban - AI Midterm")
        """
        # TODO: Khoi tao pygame va cac thuoc tinh
        pass

    def run(self):
        """
        Vong lap chinh cua game.

        Goi y:
        while running:
            1. Xu ly event (phim bam, dong cua so)
            2. Cap nhat trang thai (neu khong pause, tu dong tien buoc)
            3. Ve man hinh
            4. clock.tick(FPS)
        """
        # TODO: Implement game loop
        pass

    def handle_events(self):
        """
        Xu ly cac su kien ban phim.

        Cac phim can xu ly:
        - pygame.QUIT: thoat game
        - pygame.K_SPACE: toggle pause/resume
        - pygame.K_RIGHT: tien 1 buoc (current_step += 1)
        - pygame.K_LEFT: lui 1 buoc (current_step -= 1)

        Luu y:
        - Khi nhan Right/Left, tu dong pause
        - Kiem tra current_step khong vuot qua 0 va len(states)-1
        """
        # TODO: Xu ly events
        pass

    def draw(self):
        """
        Ve toan bo man hinh.

        Goi y:
        1. Fill background
        2. Ve ban do (tuong, san, goal)
        3. Ve boxes (phan biet box thuong va box tren goal)
        4. Ve agent
        5. Ve panel thong tin (so buoc, thuat toan, trang thai pause)
        6. pygame.display.flip()
        """
        # TODO: Ve man hinh
        pass

    def draw_cell(self, row, col, color):
        """
        Ve 1 o vuong tai vi tri (row, col) voi mau color.

        Goi y:
        rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(self.screen, color, rect)
        pygame.draw.rect(self.screen, (0,0,0), rect, 1)  # vien
        """
        # TODO: Ve 1 o
        pass

    def draw_info_panel(self):
        """
        Ve panel thong tin phia duoi hoac ben canh ban do.

        Hien thi:
        - Thuat toan dang dung (UCS / A*)
        - Buoc hien tai / tong so buoc
        - Trang thai: Dang chay / Tam dung
        - Huong dan phim

        Goi y:
        font = pygame.font.SysFont("Arial", 20)
        text = font.render("Step: 5/30", True, COLOR_TEXT)
        self.screen.blit(text, (x, y))
        """
        # TODO: Ve thong tin
        pass
