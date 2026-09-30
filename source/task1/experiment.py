# experiment.py
# So sanh do phuc tap thoi gian va khong gian giua UCS va A*

import os
import sys
import time

# Dam bao in tieng Viet tren moi console Windows/macOS khong bi loi Unicode
if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from game_map import GameMap
from state import State
from solver import Solver
from heuristic import calculate_heuristic


def run_experiments():
    """
    Chay thi nghiem so sanh hieu suat giua UCS va A* tren cac ban do:
    - Easy: 2 boxes
    - Medium: 3 boxes
    - Hard: 4 boxes
    - Sample (example_map.txt): 7 boxes
    """
    maps = [
        ("Easy",   "maps/ez_map.txt",   2),
        ("Medium", "maps/med_map.txt",  3),
        ("Hard",   "maps/hard_map.txt",  4),
        ("Sample", "maps/example_map.txt", 7),
    ]

    results = []

    print("=" * 80)
    print("THI NGHIEM SO SANH HIEU SUAT UCS VS A*")
    print("=" * 80)

    for map_name, filepath, num_boxes in maps:
        if not os.path.exists(filepath):
            print(f"Bỏ qua '{map_name}': Không tìm thấy file {filepath}")
            continue

        print(f"\n[+] Đang chạy thử nghiệm trên bản đồ: {map_name} ({num_boxes} boxes)...")
        game_map = GameMap(filepath)
        init_state = State(game_map.agent_pos, game_map.boxes)

        # --------------------------------------------------------
        # 1. Chay UCS (co timeout an toan 10s cho cac map qua lon)
        # --------------------------------------------------------
        solver_ucs = Solver(game_map)
        t_start = time.time()
        # Voi Sample (7 boxes), UCS kham pha khong gian cuc lon (>10^7 states), dat timeout 10s
        res_ucs = solver_ucs.solve_ucs(init_state, max_nodes=50000, timeout=10.0)
        t_ucs = time.time() - t_start

        ucs_data = {
            "time": t_ucs,
            "nodes": solver_ucs.nodes_expanded,
            "frontier": solver_ucs.max_frontier_size,
            "cost": res_ucs[1] if res_ucs else None,
            "timed_out": solver_ucs.timed_out
        }

        # --------------------------------------------------------
        # 2. Chay A* (Heuristic: BFS + Hungarian)
        # --------------------------------------------------------
        h_func = lambda st: calculate_heuristic(st, game_map)
        solver_astar = Solver(game_map, heuristic_func=h_func)
        t_start = time.time()
        res_astar = solver_astar.solve_astar(init_state, timeout=30.0)
        t_astar = time.time() - t_start

        astar_data = {
            "time": t_astar,
            "nodes": solver_astar.nodes_expanded,
            "frontier": solver_astar.max_frontier_size,
            "cost": res_astar[1] if res_astar else None,
            "timed_out": solver_astar.timed_out
        }

        results.append((map_name, num_boxes, ucs_data, astar_data))

    # ========================================================
    # IN KET QUA BANG SO SANH (Phuc vu bao cao va slide)
    # ========================================================
    print("\n" + "=" * 90)
    print("BANG KET QUA THI NGHIEM DO PHUC TAP THOI GIAN VA KHONG GIAN")
    print("=" * 90)

    header = f"{'Ban do':<10} | {'Thuat toan':<10} | {'Thoi gian (s)':<15} | {'Nodes Expanded':<16} | {'Max Frontier':<15} | {'Cost':<6}"
    print(header)
    print("-" * len(header))

    for map_name, num_boxes, ucs, astar in results:
        # UCS Row
        if ucs["timed_out"]:
            ucs_time_str = f"> {ucs['time']:.2f} (Timeout)"
            ucs_nodes_str = f"> {ucs['nodes']}"
            ucs_cost_str = "N/A"
        elif ucs["cost"] is not None:
            ucs_time_str = f"{ucs['time']:.4f}"
            ucs_nodes_str = f"{ucs['nodes']}"
            ucs_cost_str = f"{ucs['cost']}"
        else:
            ucs_time_str = "Fail"
            ucs_nodes_str = f"{ucs['nodes']}"
            ucs_cost_str = "None"

        print(f"{map_name:<10} | {'UCS':<10} | {ucs_time_str:<15} | {ucs_nodes_str:<16} | {ucs['frontier']:<15} | {ucs_cost_str:<6}")

        # A* Row
        astar_time_str = f"{astar['time']:.4f}" if not astar["timed_out"] else "> Timeout"
        astar_nodes_str = f"{astar['nodes']}"
        astar_cost_str = f"{astar['cost']}"
        print(f"{'':<10} | {'A*':<10} | {astar_time_str:<15} | {astar_nodes_str:<16} | {astar['frontier']:<15} | {astar_cost_str:<6}")

        # So sanh
        if ucs["cost"] is not None and astar["cost"] is not None:
            cost_match = "PASS (Cung chi phi toi uu)" if ucs["cost"] == astar["cost"] else "FAIL"
            speedup = (ucs["nodes"] / astar["nodes"]) if astar["nodes"] > 0 else 1
            print(f"{'':<10} | {'Danh gia':<10} | Cost: {cost_match} | A* giam {speedup:.1f}x so node so voi UCS")
        elif ucs["timed_out"]:
            print(f"{'':<10} | {'Danh gia':<10} | UCS bung no khong gian trang thai; A* giai quyet tot nho Heuristic.")

        print("-" * len(header))


if __name__ == "__main__":
    run_experiments()
