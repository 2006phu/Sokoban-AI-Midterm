# solver.py
# Thanh vien A phu trach
# Class chua thuat toan UCS va A*

import heapq

class Solver:
    """
    Giai bai toan Sokoban bang UCS hoac A*.

    Attributes:
        game_map:   doi tuong GameMap
        heuristic:  ham heuristic (chi dung cho A*)
    """

    def __init__(self, game_map, heuristic_func=None):
        """
        Args:
            game_map: doi tuong GameMap da doc ban do
            heuristic_func: ham tinh heuristic, nhan State tra ve so
                            None neu dung UCS
        """
        self.game_map = game_map
        self.heuristic = heuristic_func

        # Bien de do luong (dung cho experiment - Req 3)
        self.nodes_expanded = 0      # So node da mo rong
        self.max_frontier_size = 0   # Kich thuoc frontier lon nhat
        self.solution_cost = 0       # Tong chi phi loi giai

    def solve_ucs(self, initial_state):
        """
        Uniform Cost Search.

        Thuat toan:
        1. Tao priority queue (frontier), them (cost, state) ban dau
        2. Tao set explored = rong
        3. Tao dict de truy vet duong di: came_from[state] = (parent_state, action)

        4. While frontier khong rong:
            a. Pop state co cost NHO NHAT
            b. Neu la goal -> truy vet duong di -> return
            c. Them vao explored
            d. Voi moi successor:
                - Neu chua trong explored:
                  + Tinh cost moi = cost hien tai + step cost
                  + Them vao frontier

        Returns:
            (actions, total_cost)
            actions: list cac hanh dong, vd ["North", "East", ...]
            total_cost: tong chi phi

        Luu y:
        - Dung heapq de lam priority queue
        - heapq.heappush(frontier, (priority, state))
        - heapq.heappop(frontier) -> (priority, state)
        - Nho cap nhat self.nodes_expanded va self.max_frontier_size
        """
        # TODO: Implement UCS
        # Buoc 1: Khoi tao frontier, explored, came_from
        # Buoc 2: Vong lap while frontier
        # Buoc 3: Pop, kiem tra goal, expand
        # Buoc 4: Truy vet duong di khi tim thay goal
        pass

    def solve_astar(self, initial_state):
        """
        A* Search.

        GIONG UCS nhung priority = g(n) + h(n) thay vi chi g(n)

        Thuat toan:
        1. Tao frontier, them (f_score, state) ban dau
           voi f_score = 0 + heuristic(initial_state)
        2. Tao explored = rong
        3. Tao came_from va g_score dict

        4. While frontier khong rong:
            a. Pop state co f NHO NHAT
            b. Neu la goal -> truy vet -> return
            c. Them vao explored
            d. Voi moi successor:
                - g_new = g(current) + step_cost
                - f_new = g_new + heuristic(successor)
                - Neu successor chua trong explored va (chua trong frontier
                  hoac co g tot hon) -> them/cap nhat frontier

        Returns:
            (actions, total_cost)

        Luu y:
        - self.heuristic(state) tra ve gia tri h(n)
        - Ket qua total_cost PHAI BANG voi UCS (vi ca hai deu optimal)
        """
        # TODO: Implement A*
        # Tuong tu UCS nhung them h(n) vao priority
        pass

    def _reconstruct_path(self, came_from, goal_state):
        """
        Truy vet duong di tu goal ve start.

        Args:
            came_from: dict {state: (parent_state, action)}
            goal_state: trang thai dich

        Returns:
            list of actions tu start den goal

        Goi y:
        - Bat dau tu goal_state
        - Truy nguoc came_from cho den khi gap None (start)
        - Dao nguoc danh sach actions
        """
        # TODO: Truy vet va tra ve list actions
        pass
