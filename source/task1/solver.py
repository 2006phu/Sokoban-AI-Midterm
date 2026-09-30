# solver.py
# Thanh vien A phu trach
# Class chua thuat toan UCS va A*
#
# Anh xa tu ma gia BFS slide (trang 6) sang Python:
# - frontier = Priority Queue (heapq) thay vi FIFO
# - explored = set()
# - came_from = dict de truy vet duong di

import heapq
import itertools


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

        Dua tren ma gia BFS slide (trang 6) nhung dung Priority Queue:
        - BFS:  frontier = FIFO queue, POP lay dau hang doi
        - UCS:  frontier = Priority Queue, POP lay node co g(n) nho nhat

        Ma gia (anh xa tu slide):
            node <- STATE = initial, PATH-COST = 0
            frontier <- priority queue voi (g_cost, counter, state)
            explored <- empty set

            loop do:
                if EMPTY?(frontier) then return failure
                node <- POP(frontier)          # lay node co g nho nhat
                add node.STATE to explored

                if GOAL-TEST(node.STATE) then return SOLUTION(node)

                for each action in ACTIONS(node.STATE) do:
                    child <- CHILD-NODE(problem, node, action)
                    if child.STATE not in explored then
                        INSERT(child, frontier)

        Returns:
            (actions, total_cost) neu tim thay loi giai
            None neu khong tim thay
        """
        # Reset do luong
        self.nodes_expanded = 0
        self.max_frontier_size = 0

        # counter de pha vo tie khi 2 state co cung g (tranh loi so sanh State)
        counter = itertools.count()

        # frontier <- priority queue voi node ban dau
        frontier = []
        heapq.heappush(frontier, (0, next(counter), initial_state))

        # explored <- empty set
        explored = set()

        # came_from de truy vet duong di: {state: (parent_state, action)}
        came_from = {}

        # g_scores de luu g(n) tot nhat cho moi state
        g_scores = {initial_state: 0}

        # loop do
        while frontier:
            # Cap nhat do luong max frontier
            if len(frontier) > self.max_frontier_size:
                self.max_frontier_size = len(frontier)

            # node <- POP(frontier) — lay node co g nho nhat
            g_cost, _, current = heapq.heappop(frontier)

            # Bo qua neu da explored (lazy deletion)
            if current in explored:
                continue

            # add node.STATE to explored
            explored.add(current)
            self.nodes_expanded += 1

            # if GOAL-TEST(node.STATE) then return SOLUTION(node)
            if current.is_goal(self.game_map.goals):
                actions = self._reconstruct_path(came_from, current)
                self.solution_cost = g_cost
                return (actions, g_cost)

            # for each action in ACTIONS(node.STATE) do
            for action, child_state, step_cost in current.get_successors(self.game_map):
                # if child.STATE not in explored
                if child_state not in explored:
                    new_g = g_cost + step_cost

                    # Chi them neu chua co hoac tim duoc g tot hon
                    if child_state not in g_scores or new_g < g_scores[child_state]:
                        g_scores[child_state] = new_g
                        came_from[child_state] = (current, action)
                        # INSERT(child, frontier)
                        heapq.heappush(frontier, (new_g, next(counter), child_state))

        # return failure
        return None

    def solve_astar(self, initial_state):
        """
        A* Search.

        GIONG UCS nhung priority = f(n) = g(n) + h(n) thay vi chi g(n).

        Diem khac duy nhat so voi UCS:
        - Khi push vao frontier: priority = new_g + h(child_state)
        - Tuple trong heap: (f_cost, g_cost, counter, state)

        Returns:
            (actions, total_cost) neu tim thay loi giai
            None neu khong tim thay
        """
        # Reset do luong
        self.nodes_expanded = 0
        self.max_frontier_size = 0

        counter = itertools.count()

        # Tinh h cho state ban dau
        h_init = self.heuristic(initial_state)

        # frontier voi priority = f = g + h
        frontier = []
        heapq.heappush(frontier, (h_init, 0, next(counter), initial_state))

        explored = set()
        came_from = {}
        g_scores = {initial_state: 0}

        while frontier:
            if len(frontier) > self.max_frontier_size:
                self.max_frontier_size = len(frontier)

            # Pop state co f nho nhat
            f_cost, g_cost, _, current = heapq.heappop(frontier)

            if current in explored:
                continue

            explored.add(current)
            self.nodes_expanded += 1

            if current.is_goal(self.game_map.goals):
                actions = self._reconstruct_path(came_from, current)
                self.solution_cost = g_cost
                return (actions, g_cost)

            for action, child_state, step_cost in current.get_successors(self.game_map):
                if child_state not in explored:
                    new_g = g_cost + step_cost

                    if child_state not in g_scores or new_g < g_scores[child_state]:
                        g_scores[child_state] = new_g
                        # DIEM KHAC DUY NHAT: them h(n) vao priority
                        h = self.heuristic(child_state)
                        f = new_g + h
                        came_from[child_state] = (current, action)
                        heapq.heappush(frontier, (f, new_g, next(counter), child_state))

        return None

    def _reconstruct_path(self, came_from, goal_state):
        """
        Truy vet duong di tu goal ve start.

        Tuong ung SOLUTION(node) trong ma gia:
        - Bat dau tu goal_state
        - Truy nguoc came_from cho den khi khong con parent
        - Dao nguoc danh sach actions

        Args:
            came_from: dict {state: (parent_state, action)}
            goal_state: trang thai dich

        Returns:
            list of actions tu start den goal, vd ["North", "East", ...]
        """
        actions = []
        current = goal_state

        while current in came_from:
            parent, action = came_from[current]
            actions.append(action)
            current = parent

        actions.reverse()
        return actions
