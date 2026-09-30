# main.py
# Thanh vien A phu trach
# Chuong trinh chinh - entry point cua Sokoban
#
# Flow:
# 1. Doc ban do (GameMap)
# 2. Tao trang thai ban dau (State)
# 3. Hoi user chon thuat toan (UCS / A* / View mode)
# 4. Chay solver
# 5. Tao chuoi states tu loi giai
# 6. Khoi chay GUI pygame

import time
from game_map import GameMap
from state import State
from solver import Solver
from heuristic import calculate_heuristic
from gui import GameGUI, generate_state_sequence


def main():
    """Chuong trinh chinh Sokoban."""

    # ============================================
    # 1. DOC BAN DO
    # ============================================
    map_file = "maps/example_map.txt"
    print("=== SOKOBAN — AI MIDTERM ===")
    print(f"Dang doc ban do: {map_file}")

    game_map = GameMap(map_file)
    initial_state = State(game_map.agent_pos, game_map.boxes)

    # In ban do ra console
    print()
    game_map.print_map(game_map.agent_pos, game_map.boxes)
    print(f"\nAgent: {game_map.agent_pos}")
    print(f"Boxes ({len(game_map.boxes)}): {game_map.boxes}")
    print(f"Goals ({len(game_map.goals)}): {game_map.goals}")
    print(f"Map size: {game_map.rows} x {game_map.cols}")
    print()

    # ============================================
    # 2. CHON THUAT TOAN
    # ============================================
    print("Chon thuat toan:")
    print("  1. UCS (Uniform Cost Search)")
    print("  2. A* (A-Star Search)")
    print("  0. Xem ban do (khong giai)")
    choice = input("\nNhap lua chon (0/1/2): ").strip()

    if choice == "0":
        # Che do xem ban do
        gui = GameGUI(
            game_map=game_map,
            solution_actions=[],
            solution_states=[initial_state],
            algorithm_name="View Mode",
            total_cost=0,
            nodes_expanded=0
        )
        gui.run()
        return

    # ============================================
    # 3. CHAY SOLVER
    # ============================================
    if choice == "2":
        algo_name = "A*"
        h_func = lambda s: calculate_heuristic(s, game_map)
        solver = Solver(game_map, heuristic_func=h_func)
        print(f"\nDang giai bang A*...")
    else:
        algo_name = "UCS"
        solver = Solver(game_map)
        print(f"\nDang giai bang UCS...")

    start_time = time.time()
    result = solver.solve_ucs(initial_state) if algo_name == "UCS" \
             else solver.solve_astar(initial_state)
    elapsed = time.time() - start_time

    # ============================================
    # 4. HIEN THI KET QUA
    # ============================================
    if result is None:
        print("Khong tim duoc loi giai!")
        print("(Ban do co the bi deadlock hoac qua phuc tap)")
        return

    actions, cost = result

    print(f"\n=== KET QUA ===")
    print(f"Thuat toan:      {algo_name}")
    print(f"So buoc (actions): {len(actions)}")
    print(f"Tong chi phi:    {cost}")
    print(f"Nodes expanded:  {solver.nodes_expanded}")
    print(f"Max frontier:    {solver.max_frontier_size}")
    print(f"Thoi gian:       {elapsed:.4f}s")
    print(f"Actions: {actions}")

    # ============================================
    # 5. TAO CHUOI STATES & CHAY GUI
    # ============================================
    states = generate_state_sequence(initial_state, actions, game_map)

    print(f"\nDang khoi dong GUI pygame...")
    gui = GameGUI(
        game_map=game_map,
        solution_actions=actions,
        solution_states=states,
        algorithm_name=algo_name,
        total_cost=cost,
        nodes_expanded=solver.nodes_expanded
    )
    gui.run()


if __name__ == "__main__":
    main()
