# experiment.py
# Thanh vien B phu trach (Req 3)
# So sanh hieu suat UCS vs A*

import time

# Import cac module can thiet
# from game_map import GameMap
# from state import State
# from solver import Solver
# from heuristic import calculate_heuristic


def run_experiment(map_file):
    """
    Chay thi nghiem so sanh UCS va A* tren 1 ban do.

    Do luong:
    1. Thoi gian chay (giay)
    2. So node da mo rong (nodes expanded)
    3. Kich thuoc frontier lon nhat (peak memory)
    4. Tong chi phi loi giai (solution cost)

    Goi y:
    - Dung time.time() de do thoi gian
    - Lay so lieu tu solver.nodes_expanded, solver.max_frontier_size
    - Chay UCS truoc, roi A*, tren CUNG ban do
    """
    # TODO: Implement
    # Buoc 1: Doc ban do
    # game_map = GameMap(map_file)
    # initial = State(game_map.agent_pos, game_map.boxes)

    # Buoc 2: Chay UCS
    # solver_ucs = Solver(game_map)
    # start_time = time.time()
    # actions_ucs, cost_ucs = solver_ucs.solve_ucs(initial)
    # time_ucs = time.time() - start_time

    # Buoc 3: Chay A*
    # h_func = lambda s: calculate_heuristic(s, game_map)
    # solver_astar = Solver(game_map, heuristic_func=h_func)
    # start_time = time.time()
    # actions_astar, cost_astar = solver_astar.solve_astar(initial)
    # time_astar = time.time() - start_time

    # Buoc 4: In ket qua
    # print("=" * 50)
    # print(f"Ban do: {map_file}")
    # print("=" * 50)
    # print(f"{'Metric':<25} {'UCS':<15} {'A*':<15}")
    # print("-" * 55)
    # print(f"{'Thoi gian (s)':<25} {time_ucs:<15.4f} {time_astar:<15.4f}")
    # print(f"{'Nodes expanded':<25} {solver_ucs.nodes_expanded:<15} {solver_astar.nodes_expanded:<15}")
    # print(f"{'Max frontier':<25} {solver_ucs.max_frontier_size:<15} {solver_astar.max_frontier_size:<15}")
    # print(f"{'Solution cost':<25} {cost_ucs:<15} {cost_astar:<15}")

    # Buoc 5: Kiem tra cost phai bang nhau
    # assert cost_ucs == cost_astar, "LOI: Cost khac nhau!"
    # print(f"\nKiem tra: Cost UCS == Cost A*: {'PASS' if cost_ucs == cost_astar else 'FAIL'}")

    pass


def run_all_experiments():
    """
    Chay thi nghiem tren nhieu ban do khac nhau.

    Goi y:
    - Tao nhieu ban do voi do kho tang dan (it box -> nhieu box)
    - Luu ket qua vao bang
    - Ve bieu do so sanh (tuy chon, dung matplotlib)
    """
    map_files = [
        "maps/example_map.txt",
        # TODO: Them cac ban do khac de so sanh
        # "maps/easy_map.txt",
        # "maps/medium_map.txt",
        # "maps/hard_map.txt",
    ]

    for map_file in map_files:
        run_experiment(map_file)
        print()


if __name__ == "__main__":
    run_all_experiments()
