# heuristic_verification.py
# Thanh vien B phu trach (Req 4)
# Kiem chung tinh admissible va consistent cua heuristic

# from game_map import GameMap
# from state import State
# from solver import Solver
# from heuristic import calculate_heuristic


def verify_admissible(game_map, initial_state):
    """
    Kiem chung tinh admissible: h(n) <= h*(n) cho moi state n.

    Phuong phap:
    1. Chay UCS de tim loi giai toi uu -> duoc h*(start) = optimal_cost
    2. Trong qua trinh UCS, voi moi state n da xet:
       - g(n) = chi phi tu start den n (da biet tu UCS)
       - h*(n) = optimal_cost - g(n)
         (vi g(n) + h*(n) = optimal_cost cho moi state tren duong di toi uu)
       - Tinh h(n) bang heuristic cua ta
       - Kiem tra: h(n) <= h*(n)
    3. Bao cao ket qua

    Luu y QUAN TRONG:
    - Cach tinh h*(n) = optimal_cost - g(n) CHI DUNG cho state
      TREN DUONG DI TOI UU. Doi voi state KHONG tren duong di toi uu,
      can chay UCS rieng tu state do den goal de tinh h*(n) chinh xac.
    - Tuy nhien, de don gian, co the chi kiem tra tren duong di toi uu
      va 1 so state ngau nhien.

    Returns:
        True neu admissible, False neu vi pham
    """
    # TODO: Implement
    # Buoc 1: Chay UCS
    # solver = Solver(game_map)
    # actions, optimal_cost = solver.solve_ucs(initial_state)

    # Buoc 2: Truy vet cac state tren duong di toi uu
    # states = generate_states_from_actions(initial_state, actions, game_map)

    # Buoc 3: Kiem tra tung state
    # violations = 0
    # for step, state in enumerate(states):
    #     g_n = step  # chi phi tu start den state nay
    #     h_star_n = optimal_cost - g_n  # chi phi toi uu con lai
    #     h_n = calculate_heuristic(state, game_map)
    #     
    #     if h_n > h_star_n:
    #         print(f"VI PHAM admissible tai step {step}: h(n)={h_n} > h*(n)={h_star_n}")
    #         violations += 1

    # Buoc 4: Bao cao
    # print(f"Tong so state kiem tra: {len(states)}")
    # print(f"So vi pham: {violations}")
    # print(f"Ket luan: {'ADMISSIBLE' if violations == 0 else 'KHONG ADMISSIBLE'}")
    pass


def verify_consistent(game_map, initial_state):
    """
    Kiem chung tinh consistent: h(n) <= c(n, n') + h(n') cho moi cap ke.

    Phuong phap:
    1. Chay A* (hoac UCS)
    2. Voi moi cap (parent, child) trong qua trinh tim kiem:
       - Tinh h(parent) va h(child)
       - Kiem tra: h(parent) <= c(parent, child) + h(child)
       - Voi c = 1 (moi buoc chi phi 1)
       - Tuc la: h(parent) - h(child) <= 1

    Returns:
        True neu consistent, False neu vi pham
    """
    # TODO: Implement
    # Buoc 1: Chay UCS de duyet cac state
    # Buoc 2: Voi moi state, lay cac successor
    # Buoc 3: Tinh h(state) va h(successor)
    # Buoc 4: Kiem tra h(state) - h(successor) <= 1
    # Buoc 5: Bao cao ket qua

    # Luu y: Can sua solver.py de luu lai cac cap (parent, child)
    # hoac duyet lai tu dau bang BFS/UCS va kiem tra tung cap
    pass


if __name__ == "__main__":
    # TODO:
    # game_map = GameMap("maps/example_map.txt")
    # initial = State(game_map.agent_pos, game_map.boxes)
    # 
    # print("=== KIEM CHUNG ADMISSIBLE ===")
    # verify_admissible(game_map, initial)
    # 
    # print("\n=== KIEM CHUNG CONSISTENT ===")
    # verify_consistent(game_map, initial)
    pass
