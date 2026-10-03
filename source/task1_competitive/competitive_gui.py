# competitive_gui.py
# Giao dien thi dau 2 agent bang Pygame

import pygame
import sys

# ============================================================
# HANG SO MAU SAC
# ============================================================
COLOR_BG          = (35, 35, 45)
COLOR_WALL        = (100, 85, 70)
COLOR_WALL_DARK   = (75, 60, 50)
COLOR_FLOOR       = (225, 210, 185)
COLOR_FLOOR_LINE  = (200, 185, 160)
COLOR_GOAL        = (240, 140, 160)

# Mau sac Agent 1 (Xanh duong) & Agent 2 (Do cam)
COLOR_AGENT_1     = (40, 140, 240)      # Xanh duong dam
COLOR_AGENT_1_RING= (20, 90, 180)
COLOR_AGENT_2     = (240, 80, 50)       # Do cam dam
COLOR_AGENT_2_RING= (180, 40, 20)

# Mau sac Hop (Box):
COLOR_BOX_NEUTRAL = (190, 120, 50)      # Nau cam (chua ai chiem)
COLOR_BOX_AGENT_1 = (50, 180, 240)      # Xanh sang (Agent 1 da day vao goal)
COLOR_BOX_AGENT_2 = (245, 110, 70)      # Cam do (Agent 2 da day vao goal)
COLOR_BOX_BORDER  = (60, 50, 40)

# Panel & Chu
COLOR_PANEL_BG    = (28, 28, 36)
COLOR_PANEL_LINE  = (55, 55, 70)
COLOR_TEXT_WHITE  = (240, 240, 240)
COLOR_TEXT_DIM    = (150, 150, 165)
COLOR_TEXT_A1     = (80, 190, 255)
COLOR_TEXT_A2     = (255, 110, 90)
COLOR_WINNER_A1   = (40, 200, 255)
COLOR_WINNER_A2   = (255, 100, 60)
COLOR_DRAW        = (255, 215, 0)

CELL_SIZE         = 50
PANEL_HEIGHT      = 130
FPS               = 60
AUTO_STEP_DELAY   = 450  # ms moi buoc tu dong


class CompetitiveGUI:
    """
    Giao dien thi dau 2 agent bang Pygame.
    """

    def __init__(self, game_map, agent1, agent2, step_limit=50):
        self.game_map = game_map
        self.agent1 = agent1
        self.agent2 = agent2
        self.step_limit = step_limit

        from state import CompetitiveState
        self.initial_state = CompetitiveState(
            pos1=game_map.agent1_pos,
            pos2=game_map.agent2_pos,
            boxes=game_map.boxes,
            step_limit=step_limit
        )
        self.state = self.initial_state

        # Lich su buoc
        self.history = [self.initial_state]
        self.action_history = []
        self.current_idx = 0

        self.paused = True
        self.running = True
        self.last_step_time = 0

        # Kich thuoc cua so
        self.board_width = game_map.cols * CELL_SIZE
        self.board_height = game_map.rows * CELL_SIZE
        self.window_width = max(self.board_width, 640)
        self.window_height = self.board_height + PANEL_HEIGHT

        self.offset_x = (self.window_width - self.board_width) // 2
        self.offset_y = 0

        pygame.init()
        pygame.display.set_caption("Sokoban — 2-Agent Competitive Mode")
        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        self.clock = pygame.time.Clock()

        # Font cross-platform Windows / macOS Ventura
        fonts = "consolas,menlo,monaco,dejavusans,couriernew,arial"
        self.font_title = pygame.font.SysFont(fonts, 22, bold=True)
        self.font_score = pygame.font.SysFont(fonts, 20, bold=True)
        self.font_text  = pygame.font.SysFont(fonts, 16)
        self.font_small = pygame.font.SysFont(fonts, 13)

    def run(self):
        while self.running:
            self._handle_events()
            self._update()
            self._draw()
            self.clock.tick(FPS)
        pygame.quit()

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

                elif event.key == pygame.K_SPACE:
                    if not self.state.is_game_over():
                        self.paused = not self.paused

                elif event.key == pygame.K_RIGHT:
                    self.paused = True
                    self._step_next()

                elif event.key == pygame.K_LEFT:
                    self.paused = True
                    if self.current_idx > 0:
                        self.current_idx -= 1
                        self.state = self.history[self.current_idx]

                elif event.key == pygame.K_r:
                    # Reset game
                    self.state = self.initial_state
                    self.history = [self.initial_state]
                    self.action_history = []
                    self.current_idx = 0
                    self.paused = True

    def _update(self):
        if not self.paused and not self.state.is_game_over():
            now = pygame.time.get_ticks()
            if now - self.last_step_time >= AUTO_STEP_DELAY:
                self.last_step_time = now
                self._step_next()

    def _step_next(self):
        """Yeu cau ca 2 agent ra quyet dinh dong thoi va thuc hien buoc tiep theo."""
        if self.state.is_game_over():
            self.paused = True
            return

        # Neu dang xem lai lich su -> chi tien buoc
        if self.current_idx < len(self.history) - 1:
            self.current_idx += 1
            self.state = self.history[self.current_idx]
            return

        # Tao game_state cho Agent 1
        goals = self.game_map.goals
        s1 = self.state.get_score(1, goals)
        s2 = self.state.get_score(2, goals)
        steps_left = self.step_limit - self.state.step

        env_a1 = {
            "my_pos": self.state.pos1,
            "opponent_pos": self.state.pos2,
            "boxes": set(self.state.boxes),
            "my_boxes_on_goal": s1,
            "opponent_boxes_on_goal": s2,
            "goals": goals,
            "walls": self.game_map.walls,
            "steps_remaining": steps_left,
            "box_ownership": dict(self.state.box_ownership),
            "my_id": 1,
            "opponent_id": 2,
        }

        env_a2 = {
            "my_pos": self.state.pos2,
            "opponent_pos": self.state.pos1,
            "boxes": set(self.state.boxes),
            "my_boxes_on_goal": s2,
            "opponent_boxes_on_goal": s1,
            "goals": goals,
            "walls": self.game_map.walls,
            "steps_remaining": steps_left,
            "box_ownership": dict(self.state.box_ownership),
            "my_id": 2,
            "opponent_id": 1,
        }

        # Ca hai agent hanh dong dong thoi
        act1 = self.agent1.choose_action(env_a1)
        act2 = self.agent2.choose_action(env_a2)

        next_state = self.state.resolve_step(act1, act2, self.game_map)
        self.state = next_state
        self.history.append(next_state)
        self.action_history.append((act1, act2))
        self.current_idx += 1

    # ========================================================
    # VE GIAO DIEN
    # ========================================================
    def _draw(self):
        self.screen.fill(COLOR_BG)
        self._draw_board()
        self._draw_panel()
        pygame.display.flip()

    def _draw_board(self):
        # 1. Ve nen tuong va san
        for r in range(self.game_map.rows):
            for c in range(self.game_map.cols):
                pos = (r, c)
                x = self.offset_x + c * CELL_SIZE
                y = self.offset_y + r * CELL_SIZE

                if pos in self.game_map.walls:
                    pygame.draw.rect(self.screen, COLOR_WALL, (x, y, CELL_SIZE, CELL_SIZE))
                    pygame.draw.rect(self.screen, COLOR_WALL_DARK, (x, y, CELL_SIZE, CELL_SIZE), 1)
                elif pos in self.game_map.floor_cells:
                    pygame.draw.rect(self.screen, COLOR_FLOOR, (x, y, CELL_SIZE, CELL_SIZE))
                    pygame.draw.rect(self.screen, COLOR_FLOOR_LINE, (x, y, CELL_SIZE, CELL_SIZE), 1)

                    if pos in self.game_map.goals:
                        center = (x + CELL_SIZE // 2, y + CELL_SIZE // 2)
                        pygame.draw.circle(self.screen, COLOR_GOAL, center, CELL_SIZE // 5)
                        pygame.draw.circle(self.screen, (255, 200, 220), (center[0] - 2, center[1] - 2), 3)

        # 2. Ve cac Hop (Boxes) voi mau rieng theo quyen so huu
        for box in self.state.boxes:
            bx = self.offset_x + box[1] * CELL_SIZE
            by = self.offset_y + box[0] * CELL_SIZE
            owner = self.state.box_ownership.get(box, None)

            # Mau sac box theo agent so huu
            if box in self.game_map.goals and owner == 1:
                color = COLOR_BOX_AGENT_1
                tag = "1"
            elif box in self.game_map.goals and owner == 2:
                color = COLOR_BOX_AGENT_2
                tag = "2"
            else:
                color = COLOR_BOX_NEUTRAL
                tag = ""

            margin = 5
            rect = pygame.Rect(bx + margin, by + margin, CELL_SIZE - 2 * margin, CELL_SIZE - 2 * margin)
            pygame.draw.rect(self.screen, color, rect, border_radius=4)
            pygame.draw.rect(self.screen, COLOR_BOX_BORDER, rect, 2, border_radius=4)

            # Ve nhan 1 / 2 tren hop
            if tag:
                lbl = self.font_small.render(f"P{tag}", True, (255, 255, 255))
                self.screen.blit(lbl, (bx + (CELL_SIZE - lbl.get_width()) // 2, by + (CELL_SIZE - lbl.get_height()) // 2))

        # 3. Ve Agent 1 (Xanh) va Agent 2 (Do)
        self._draw_agent_token(self.state.pos1, COLOR_AGENT_1, COLOR_AGENT_1_RING, "1")
        self._draw_agent_token(self.state.pos2, COLOR_AGENT_2, COLOR_AGENT_2_RING, "2")

    def _draw_agent_token(self, pos, fill_color, ring_color, label):
        cx = self.offset_x + pos[1] * CELL_SIZE + CELL_SIZE // 2
        cy = self.offset_y + pos[0] * CELL_SIZE + CELL_SIZE // 2
        r = CELL_SIZE // 3

        pygame.draw.circle(self.screen, fill_color, (cx, cy), r)
        pygame.draw.circle(self.screen, ring_color, (cx, cy), r, 2)

        lbl = self.font_score.render(label, True, (255, 255, 255))
        self.screen.blit(lbl, (cx - lbl.get_width() // 2, cy - lbl.get_height() // 2))

    def _draw_panel(self):
        py = self.board_height
        panel_rect = pygame.Rect(0, py, self.window_width, PANEL_HEIGHT)
        pygame.draw.rect(self.screen, COLOR_PANEL_BG, panel_rect)
        pygame.draw.line(self.screen, COLOR_PANEL_LINE, (0, py), (self.window_width, py), 2)

        # Diem so
        s1 = self.state.get_score(1, self.game_map.goals)
        s2 = self.state.get_score(2, self.game_map.goals)

        # Cot 1: Agent 1 Score
        t_a1 = self.font_title.render("AGENT 1 (Blue)", True, COLOR_TEXT_A1)
        s_a1 = self.font_score.render(f"Boxes on Goal: {s1}", True, COLOR_TEXT_WHITE)
        self.screen.blit(t_a1, (20, py + 12))
        self.screen.blit(s_a1, (20, py + 42))

        # Cot 3: Agent 2 Score
        t_a2 = self.font_title.render("AGENT 2 (Red)", True, COLOR_TEXT_A2)
        s_a2 = self.font_score.render(f"Boxes on Goal: {s2}", True, COLOR_TEXT_WHITE)
        self.screen.blit(t_a2, (self.window_width - t_a2.get_width() - 20, py + 12))
        self.screen.blit(s_a2, (self.window_width - s_a2.get_width() - 20, py + 42))

        # Cot Giua: So buoc & Trang thai
        step_str = f"Step: {self.state.step} / {self.step_limit}"
        t_step = self.font_title.render(step_str, True, COLOR_TEXT_WHITE)
        self.screen.blit(t_step, ((self.window_width - t_step.get_width()) // 2, py + 12))

        if self.state.is_game_over():
            win = self.state.get_winner(self.game_map.goals)
            if win == 1:
                st_msg = "WINNER: AGENT 1!"
                st_col = COLOR_WINNER_A1
            elif win == 2:
                st_msg = "WINNER: AGENT 2!"
                st_col = COLOR_WINNER_A2
            else:
                st_msg = "GAME OVER: DRAW!"
                st_col = COLOR_DRAW
        elif self.paused:
            st_msg = "PAUSED (Press SPACE to Play)"
            st_col = (255, 200, 100)
        else:
            st_msg = "COMPETING IN PROGRESS"
            st_col = (100, 240, 160)

        t_status = self.font_score.render(st_msg, True, st_col)
        self.screen.blit(t_status, ((self.window_width - t_status.get_width()) // 2, py + 42))

        # Huong dan phim
        help_str = "SPACE: Play/Pause   RIGHT: Next Step   LEFT: Back   R: Reset   ESC: Quit"
        t_help = self.font_small.render(help_str, True, COLOR_TEXT_DIM)
        self.screen.blit(t_help, ((self.window_width - t_help.get_width()) // 2, py + 95))
