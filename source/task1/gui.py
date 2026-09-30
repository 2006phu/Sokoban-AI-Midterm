# gui.py
# Thanh vien A phu trach
# Giao dien game Sokoban bang pygame (Req 5)
#
# Chuc nang yeu cau:
# 1. Chon thuat toan: UCS hoac A*
# 2. Hien thi so buoc (number of actions) tren UI
# 3. Space: pause/resume
# 4. -> (Right): tien 1 buoc
# 5. <- (Left): lui 1 buoc
# 6. OOP

import pygame
import sys

# ============================================================
# HANG SO MAU SAC
# ============================================================
COLOR_BG         = (45, 45, 55)        # Nen cua so
COLOR_WALL       = (110, 90, 70)       # Tuong nau
COLOR_WALL_DARK  = (85, 70, 55)        # Hoa tiet gach
COLOR_FLOOR      = (230, 215, 185)     # San vang nhat
COLOR_FLOOR_LINE = (210, 195, 165)     # Vien o san
COLOR_GOAL       = (255, 100, 130)     # Diem dich hong
COLOR_BOX        = (220, 140, 40)      # Hop cam
COLOR_BOX_BORDER = (180, 105, 20)      # Vien hop
COLOR_BOX_X      = (190, 110, 15)      # Dau X tren hop
COLOR_BOX_DONE   = (120, 75, 30)       # Hop da vao dich (nau dam)
COLOR_BOX_DONE_B = (90, 55, 20)        # Vien hop da vao dich
COLOR_BOX_DONE_X = (80, 45, 15)        # Dau X hop da vao dich
COLOR_AGENT      = (60, 140, 230)      # Agent xanh duong
COLOR_AGENT_DARK = (40, 100, 180)      # Vien agent
COLOR_AGENT_EYE  = (255, 255, 255)     # Mat trang
COLOR_AGENT_PUPIL = (30, 30, 30)       # Con nguoi mat
COLOR_PANEL_BG   = (35, 35, 45)        # Nen panel
COLOR_PANEL_LINE = (60, 60, 75)        # Vien panel
COLOR_TEXT        = (230, 230, 230)     # Chu trang
COLOR_TEXT_DIM    = (150, 150, 160)     # Chu mo
COLOR_TEXT_HIGH   = (100, 220, 160)     # Chu xanh la (status tot)
COLOR_TEXT_WARN   = (255, 180, 80)      # Chu cam (canh bao)

# ============================================================
# HANG SO KICH THUOC
# ============================================================
CELL_SIZE       = 64      # Pixel moi o
PANEL_HEIGHT    = 130     # Chieu cao panel thong tin
FPS             = 60      # Frame per second
AUTO_STEP_DELAY = 400     # ms giua moi buoc tu dong


class GameGUI:
    """
    Giao dien game Sokoban dung pygame.

    Chuc nang:
    - Chon thuat toan UCS / A*
    - Hien thi buoc hien tai / tong buoc
    - Space: pause/resume
    - Right arrow: tien 1 buoc
    - Left arrow: lui 1 buoc
    - R: reset ve buoc 0
    - H: mo/dong tro giup
    - ESC: thoat
    """

    def __init__(self, game_map, solution_actions=None, solution_states=None,
                 algorithm_name="UCS", total_cost=0, nodes_expanded=0):
        """
        Khoi tao GUI.

        Args:
            game_map: doi tuong GameMap
            solution_actions: list actions (co the None neu chua giai)
            solution_states: list states tuong ung moi buoc
            algorithm_name: ten thuat toan da dung
            total_cost: tong chi phi loi giai
            nodes_expanded: so node da mo rong
        """
        self.game_map = game_map
        self.actions = solution_actions if solution_actions else []
        self.states = solution_states if solution_states else []
        self.algorithm_name = algorithm_name
        self.total_cost = total_cost
        self.nodes_expanded = nodes_expanded

        # Trang thai dieu khien
        self.current_step = 0
        self.paused = True
        self.running = True
        self.last_auto_step = 0
        self.show_help = False

        # Tinh kich thuoc cua so
        self.board_width = game_map.cols * CELL_SIZE
        self.board_height = game_map.rows * CELL_SIZE
        self.window_width = max(self.board_width, 500)
        self.window_height = self.board_height + PANEL_HEIGHT

        # Offset de can giua ban do
        self.board_offset_x = (self.window_width - self.board_width) // 2
        self.board_offset_y = 0

        # Khoi tao pygame
        pygame.init()
        pygame.display.set_caption("Sokoban — AI Midterm")
        self.screen = pygame.display.set_mode(
            (self.window_width, self.window_height)
        )
        self.clock = pygame.time.Clock()

        # Font chu
        self.font_big = pygame.font.SysFont("Consolas", 22, bold=True)
        self.font_med = pygame.font.SysFont("Consolas", 17)
        self.font_sm  = pygame.font.SysFont("Consolas", 14)

    # ========================================================
    # VONG LAP CHINH
    # ========================================================
    def run(self):
        """
        Vong lap chinh cua game (game loop).

        Flow:
        1. Xu ly event (phim bam, dong cua so)
        2. Cap nhat trang thai (auto-step neu khong pause)
        3. Ve man hinh
        4. clock.tick(FPS) gioi han toc do khung hinh
        """
        while self.running:
            self._handle_events()
            self._update()
            self._draw()
            self.clock.tick(FPS)
        pygame.quit()

    # ========================================================
    # XU LY SU KIEN BAN PHIM
    # ========================================================
    def _handle_events(self):
        """
        Xu ly phim bam va su kien cua so.

        Phim:
        - QUIT / ESC: thoat
        - SPACE: pause/resume
        - RIGHT: tien 1 buoc (tu dong pause)
        - LEFT: lui 1 buoc (tu dong pause)
        - R: reset ve buoc 0
        - H: toggle help overlay
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

                elif event.key == pygame.K_SPACE:
                    # Toggle pause/resume
                    if len(self.states) > 1:
                        self.paused = not self.paused

                elif event.key == pygame.K_RIGHT:
                    # Tien 1 buoc, tu dong pause
                    self.paused = True
                    self._step_forward()

                elif event.key == pygame.K_LEFT:
                    # Lui 1 buoc, tu dong pause
                    self.paused = True
                    self._step_backward()

                elif event.key == pygame.K_r:
                    # Reset ve buoc 0
                    self.current_step = 0
                    self.paused = True

                elif event.key == pygame.K_h:
                    # Toggle help
                    self.show_help = not self.show_help

    def _step_forward(self):
        """Tien 1 buoc."""
        if self.current_step < len(self.states) - 1:
            self.current_step += 1

    def _step_backward(self):
        """Lui 1 buoc."""
        if self.current_step > 0:
            self.current_step -= 1

    # ========================================================
    # CAP NHAT TRANG THAI
    # ========================================================
    def _update(self):
        """Cap nhat tu dong khi khong pause (auto-step moi 400ms)."""
        if not self.paused and len(self.states) > 1:
            now = pygame.time.get_ticks()
            if now - self.last_auto_step >= AUTO_STEP_DELAY:
                self.last_auto_step = now
                if self.current_step < len(self.states) - 1:
                    self.current_step += 1
                else:
                    # Dung khi het buoc
                    self.paused = True

    # ========================================================
    # VE MAN HINH
    # ========================================================
    def _draw(self):
        """Ve toan bo man hinh."""
        self.screen.fill(COLOR_BG)
        self._draw_board()
        self._draw_panel()
        if self.show_help:
            self._draw_help_overlay()
        pygame.display.flip()

    def _draw_board(self):
        """Ve ban do game (tuong, san, goal, box, agent)."""
        # Lay state hien tai
        state = self.states[self.current_step] if self.states else None
        agent_pos = state.agent_pos if state else self.game_map.agent_pos
        boxes = state.boxes if state else self.game_map.boxes

        # Ve tung o tren ban do
        for row in range(self.game_map.rows):
            for col in range(self.game_map.cols):
                pos = (row, col)
                x = self.board_offset_x + col * CELL_SIZE
                y = self.board_offset_y + row * CELL_SIZE

                if pos in self.game_map.walls:
                    self._draw_wall(x, y)
                elif pos in self.game_map.floor_cells:
                    self._draw_floor(x, y)
                    if pos in self.game_map.goals:
                        self._draw_goal(x, y)

        # Ve boxes (tren lop san)
        for box in boxes:
            bx = self.board_offset_x + box[1] * CELL_SIZE
            by = self.board_offset_y + box[0] * CELL_SIZE
            on_goal = box in self.game_map.goals
            self._draw_box(bx, by, on_goal)

        # Ve agent (tren cung)
        ax = self.board_offset_x + agent_pos[1] * CELL_SIZE
        ay = self.board_offset_y + agent_pos[0] * CELL_SIZE
        self._draw_agent(ax, ay)

    # --------------------------------------------------------
    # VE TUNG THANH PHAN
    # --------------------------------------------------------
    def _draw_wall(self, x, y):
        """Ve 1 o tuong co hoa tiet gach."""
        rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(self.screen, COLOR_WALL, rect)

        # Hoa tiet gach (4 hang gach ngang)
        brick_h = CELL_SIZE // 4
        for i in range(4):
            by = y + i * brick_h
            # Duong ngang
            pygame.draw.line(
                self.screen, COLOR_WALL_DARK,
                (x, by), (x + CELL_SIZE, by), 1
            )
            # Duong doc (lech nhau giua cac hang)
            offset = CELL_SIZE // 2 if i % 2 == 0 else 0
            for j in range(3):
                bx = x + offset + j * (CELL_SIZE // 2)
                if x <= bx <= x + CELL_SIZE:
                    pygame.draw.line(
                        self.screen, COLOR_WALL_DARK,
                        (bx, by), (bx, by + brick_h), 1
                    )

        # Vien ngoai
        pygame.draw.rect(self.screen, COLOR_WALL_DARK, rect, 1)

    def _draw_floor(self, x, y):
        """Ve 1 o san."""
        rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(self.screen, COLOR_FLOOR, rect)
        pygame.draw.rect(self.screen, COLOR_FLOOR_LINE, rect, 1)

    def _draw_goal(self, x, y):
        """Ve diem dich (cham hong phat sang)."""
        center = (x + CELL_SIZE // 2, y + CELL_SIZE // 2)
        radius = CELL_SIZE // 5

        # Vong tron phat sang (glow)
        glow_surf = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
        pygame.draw.circle(
            glow_surf, (255, 100, 130, 60),
            (CELL_SIZE // 2, CELL_SIZE // 2), radius + 6
        )
        self.screen.blit(glow_surf, (x, y))

        # Cham chinh
        pygame.draw.circle(self.screen, COLOR_GOAL, center, radius)
        # Diem sang (highlight)
        pygame.draw.circle(
            self.screen, (255, 180, 190),
            (center[0] - 2, center[1] - 2), radius // 3
        )

    def _draw_box(self, x, y, on_goal):
        """Ve hop (box). Mau khac nhau khi tren goal va khi chua."""
        margin = 4
        rect = pygame.Rect(x + margin, y + margin,
                           CELL_SIZE - 2 * margin, CELL_SIZE - 2 * margin)

        if on_goal:
            color = COLOR_BOX_DONE
            border = COLOR_BOX_DONE_B
            x_color = COLOR_BOX_DONE_X
        else:
            color = COLOR_BOX
            border = COLOR_BOX_BORDER
            x_color = COLOR_BOX_X

        # Than hop (bo goc)
        pygame.draw.rect(self.screen, color, rect, border_radius=4)
        # Vien hop
        pygame.draw.rect(self.screen, border, rect, 2, border_radius=4)

        # Dau X tren hop
        inner = 12
        x1, y1 = x + margin + inner, y + margin + inner
        x2 = x + CELL_SIZE - margin - inner
        y2 = y + CELL_SIZE - margin - inner
        pygame.draw.line(self.screen, x_color, (x1, y1), (x2, y2), 3)
        pygame.draw.line(self.screen, x_color, (x2, y1), (x1, y2), 3)

        # Vien noi bat phia tren (highlight)
        highlight = pygame.Rect(x + margin + 2, y + margin + 2,
                                CELL_SIZE - 2 * margin - 4, 3)
        h_color = (255, 200, 100) if not on_goal else (160, 120, 70)
        pygame.draw.rect(self.screen, h_color, highlight, border_radius=1)

    def _draw_agent(self, x, y):
        """Ve nhan vat (agent) hinh tron xanh duong co mat cuoi."""
        cx = x + CELL_SIZE // 2
        cy = y + CELL_SIZE // 2

        # Than (hinh tron)
        body_r = CELL_SIZE // 3
        pygame.draw.circle(self.screen, COLOR_AGENT, (cx, cy), body_r)
        pygame.draw.circle(self.screen, COLOR_AGENT_DARK, (cx, cy), body_r, 2)

        # Mat trai
        eye_offset = body_r // 3
        eye_r = 5
        pupil_r = 2
        pygame.draw.circle(
            self.screen, COLOR_AGENT_EYE,
            (cx - eye_offset, cy - 3), eye_r
        )
        pygame.draw.circle(
            self.screen, COLOR_AGENT_PUPIL,
            (cx - eye_offset + 1, cy - 3), pupil_r
        )

        # Mat phai
        pygame.draw.circle(
            self.screen, COLOR_AGENT_EYE,
            (cx + eye_offset, cy - 3), eye_r
        )
        pygame.draw.circle(
            self.screen, COLOR_AGENT_PUPIL,
            (cx + eye_offset + 1, cy - 3), pupil_r
        )

        # Mieng cuoi
        smile_rect = pygame.Rect(cx - 6, cy + 2, 12, 8)
        pygame.draw.arc(
            self.screen, COLOR_AGENT_PUPIL,
            smile_rect, 3.14, 6.28, 2
        )

    # --------------------------------------------------------
    # VE PANEL THONG TIN
    # --------------------------------------------------------
    def _draw_panel(self):
        """Ve panel thong tin phia duoi ban do."""
        panel_y = self.board_height
        panel_rect = pygame.Rect(0, panel_y,
                                  self.window_width, PANEL_HEIGHT)
        pygame.draw.rect(self.screen, COLOR_PANEL_BG, panel_rect)
        pygame.draw.line(
            self.screen, COLOR_PANEL_LINE,
            (0, panel_y), (self.window_width, panel_y), 2
        )

        # --- Dong 1: Thuat toan + Trang thai ---
        y1 = panel_y + 12
        algo_text = self.font_med.render(
            f"Algorithm: {self.algorithm_name}", True, COLOR_TEXT
        )
        self.screen.blit(algo_text, (15, y1))

        # Trang thai hien tai
        if not self.states or len(self.states) <= 1:
            status = "No Solution"
            status_color = COLOR_TEXT_WARN
        elif self.current_step >= len(self.states) - 1:
            status = "COMPLETED"
            status_color = COLOR_TEXT_HIGH
        elif self.paused:
            status = "PAUSED"
            status_color = COLOR_TEXT_WARN
        else:
            status = "PLAYING"
            status_color = COLOR_TEXT_HIGH

        status_text = self.font_med.render(status, True, status_color)
        self.screen.blit(
            status_text,
            (self.window_width - status_text.get_width() - 15, y1)
        )

        # --- Dong 2: Step + Cost ---
        y2 = panel_y + 40
        total = max(len(self.states) - 1, 0)
        step_text = self.font_big.render(
            f"Step: {self.current_step} / {total}", True, COLOR_TEXT
        )
        self.screen.blit(step_text, (15, y2))

        cost_text = self.font_med.render(
            f"Cost: {self.total_cost}   Nodes: {self.nodes_expanded}",
            True, COLOR_TEXT_DIM
        )
        self.screen.blit(
            cost_text,
            (self.window_width - cost_text.get_width() - 15, y2 + 4)
        )

        # --- Dong 3: Action hien tai ---
        y3 = panel_y + 72
        if self.actions and 0 < self.current_step <= len(self.actions):
            action = self.actions[self.current_step - 1]
            arrow_map = {"North": "↑", "South": "↓",
                         "East": "→", "West": "←"}
            arrow = arrow_map.get(action, "?")
            action_str = f"Action: {arrow} {action}"
        else:
            action_str = "Action: —"
        act_text = self.font_med.render(action_str, True, COLOR_TEXT)
        self.screen.blit(act_text, (15, y3))

        # --- Dong 4: Huong dan phim ---
        y4 = panel_y + 100
        help_str = "SPACE: Play/Pause   <->: Step   R: Reset   H: Help   ESC: Quit"
        help_text = self.font_sm.render(help_str, True, COLOR_TEXT_DIM)
        self.screen.blit(
            help_text,
            ((self.window_width - help_text.get_width()) // 2, y4)
        )

    # --------------------------------------------------------
    # MAN HINH TRO GIUP
    # --------------------------------------------------------
    def _draw_help_overlay(self):
        """Ve man hinh tro giup ban trong."""
        overlay = pygame.Surface(
            (self.window_width, self.window_height), pygame.SRCALPHA
        )
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))

        lines = [
            ("SOKOBAN — HELP", self.font_big, COLOR_TEXT_HIGH),
            ("", None, None),
            ("SPACE     Play / Pause auto-step", self.font_med, COLOR_TEXT),
            ("->        Forward one step", self.font_med, COLOR_TEXT),
            ("<-        Backward one step", self.font_med, COLOR_TEXT),
            ("R         Reset to step 0", self.font_med, COLOR_TEXT),
            ("H         Toggle this help", self.font_med, COLOR_TEXT),
            ("ESC       Quit game", self.font_med, COLOR_TEXT),
            ("", None, None),
            ("Press H to close", self.font_sm, COLOR_TEXT_DIM),
        ]

        start_y = self.window_height // 2 - len(lines) * 14
        for i, (text, font, color) in enumerate(lines):
            if font is None:
                continue
            surf = font.render(text, True, color)
            tx = (self.window_width - surf.get_width()) // 2
            self.screen.blit(surf, (tx, start_y + i * 30))


# ============================================================
# HAM HO TRO
# ============================================================
def generate_state_sequence(initial_state, actions, game_map):
    """
    Tu state ban dau va list actions, tao list cac state theo tung buoc.
    Dung de gui phat lai loi giai buoc-theo-buoc.

    Args:
        initial_state: State ban dau
        actions: list cac action name, vd ["North", "East", ...]
        game_map: doi tuong GameMap

    Returns:
        list of State (bao gom state ban dau)
    """
    states = [initial_state]
    current = initial_state

    for action in actions:
        successors = current.get_successors(game_map)
        moved = False
        for name, next_state, cost in successors:
            if name == action:
                states.append(next_state)
                current = next_state
                moved = True
                break
        if not moved:
            # Action khong hop le -> giu nguyen state
            states.append(current)

    return states
