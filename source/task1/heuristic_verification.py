# heuristic_verification.py
# Thanh vien B phu trach - Req 4
# Kiem chung tinh Admissible va Consistent cua Heuristic bang thuc nghiem
# Tuan thu OOP model, tai su dung GameMap, State, Solver, HeuristicCalculator

import os
import sys
import time
from collections import deque

# Dam bao UTF-8 an toan tren Windows / macOS
if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from game_map import GameMap
from state import State
from solver import Solver
from heuristic import calculate_heuristic


def generate_sample_states(game_map, initial_state, max_states=1500):
    """
    Thu thap cac trang thai hop le co the dat toi (reachable states)
    bang cach loang BFS tu initial_state.
    """
    states = []
    queue = deque([initial_state])
    explored = {initial_state}

    while queue and len(states) < max_states:
        current = queue.popleft()
        states.append(current)

        for action, next_state, cost in current.get_successors(game_map):
            if next_state not in explored:
                explored.add(next_state)
                queue.append(next_state)

    return states


def verify_heuristic(map_file):
    """
    Kiem chung 2 tinh chat quan trong cua heuristic:
    1. Consistent (Monotonic): h(n) <= c(n, a, n') + h(n') voi moi buoc chuyen
    2. Admissible: h(n) <= h*(n) voi moi state
    """
    if not os.path.exists(map_file):
        print(f"Loi: Khong tim thay file {map_file}")
        return

    print("=" * 80)
    print("KIEM CHUNG TINH CHAT HEURISTIC (Requirement 4)")
    print("Heuristic: BFS Shortest Distance + Hungarian Algorithm (Linear Sum Assignment)")
    print(f"Ban do kiem tra: {map_file}")
    print("=" * 80)

    game_map = GameMap(map_file)
    init_state = State(game_map.agent_pos, game_map.boxes)

    print("\n[1/3] Dang thu thap cac trang thai hop le bang BFS...")
    sample_states = generate_sample_states(game_map, init_state, max_states=1500)
    print(f"-> Da thu thap duoc {len(sample_states)} trang thai mau.")

    # --------------------------------------------------------
    # PHAN 1: KIEM CHUNG TINH CONSISTENT (MONOTONIC)
    # Dieu kien: h(n) <= c(n, a, n') + h(n')
    # Vi c(n, a, n') = 1 nen tuong duong: h(n) - h(n') <= 1
    # --------------------------------------------------------
    print("\n[2/3] Dang kiem chung tinh CONSISTENT tren cac cap trang thai ke...")
    consistent_pairs = 0
    consistent_violations = 0
    max_h_diff = 0

    for state in sample_states:
        h_n = calculate_heuristic(state, game_map)
        if h_n == float('inf'):
            continue

        for action, next_state, cost in state.get_successors(game_map):
            h_next = calculate_heuristic(next_state, game_map)
            if h_next == float('inf'):
                continue

            consistent_pairs += 1
            diff = h_n - h_next
            if diff > max_h_diff:
                max_h_diff = diff

            if diff > cost:  # cost = 1
                consistent_violations += 1
                print(f"  [CANH BAO] Vi pham Consistent: h(n)={h_n}, h(n')={h_next}, c={cost}")

    print("\n--- KET QUA KIEM CHUNG CONSISTENT ---")
    print(f"- Tong so cap chuyen tiep da kiem tra: {consistent_pairs}")
    print(f"- So luong vi pham: {consistent_violations}")
    print(f"- Do lech lon nhat max(h(n) - h(n')): {max_h_diff}")
    if consistent_violations == 0:
        print("- Ket luan: HEURISTIC DAT TINH CONSISTENT (MONOTONIC) [PASS]")
    else:
        print("- Ket luan: HEURISTIC KHONG CONSISTENT [FAIL]")

    # --------------------------------------------------------
    # PHAN 2: KIEM CHUNG TINH ADMISSIBLE
    # Dieu kien: h(n) <= h*(n)
    # Tinh h*(n) bang UCS tim chi phi toi uu thuc te
    # --------------------------------------------------------
    print("\n[3/3] Dang kiem chung tinh ADMISSIBLE voi chi phi thuc h*(n)...")
    num_admissible_tests = min(60, len(sample_states))
    admissible_tested = 0
    admissible_violations = 0
    solver = Solver(game_map)

    for state in sample_states[:num_admissible_tests]:
        h_n = calculate_heuristic(state, game_map)
        if h_n == float('inf'):
            continue

        # Tinh h*(n) bang UCS tu trang thai nay den dich
        res = solver.solve_ucs(state, timeout=2.0)
        if res is not None:
            actions, h_star = res
            admissible_tested += 1

            if h_n > h_star:
                admissible_violations += 1
                print(f"  [CANH BAO] Vi pham Admissible: h(n)={h_n} > h*(n)={h_star}")

    print("\n--- KET QUA KIEM CHUNG ADMISSIBLE ---")
    print(f"- Tong so trang thai da tinh duoc h*(n) bang UCS: {admissible_tested}")
    print(f"- So luong vi pham: {admissible_violations}")
    if admissible_violations == 0:
        print("- Ket luan: HEURISTIC DAT TINH ADMISSIBLE (KHONG DANH GIA QUA CAO) [PASS]")
    else:
        print("- Ket luan: HEURISTIC KHONG ADMISSIBLE [FAIL]")

    # --------------------------------------------------------
    # TONG KET DANH GIA LY THUYET VA THUC NGHIEM
    # --------------------------------------------------------
    print("\n" + "=" * 80)
    print("TONG KET LY THUYET & THUC NGHIEM CHO BAO CAO REQ 4:")
    print("1. Tinh Admissible: BFS bo qua cac chuong ngai vat hop khac va khong tinh den")
    print("   chi phi xoay tro cua Agent, dong thoi Hungarian cho ghep cap voi tong quang")
    print("   duong nho nhat, do do h(n) luon <= h*(n) -> Heuristic admissible.")
    print("2. Tinh Consistent: Moi buoc di chi di chuyen 1 o va day toi da 1 hop 1 buoc,")
    print("   tong khoang cach ngan nhat den cac goal chi giam toi da 1 -> h(n) - h(n') <= 1.")
    print("   Heuristic nhat quan (consistent) dam bao A* luon tim loi giai toi uu.")
    print("=" * 80)


if __name__ == "__main__":
    test_map = "maps/ez_map.txt"
    verify_heuristic(test_map)
