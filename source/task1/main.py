# main.py
# Entry point cua chuong trinh Sokoban
# Thanh vien A phu trach

from game_map import GameMap
from state import State
from solver import Solver
from heuristic import calculate_heuristic
from gui import GameGUI


def main():
    """
    Chuong trinh chinh.

    Luong xu ly:
    1. Doc ban do tu file
    2. Cho user chon thuat toan (UCS / A*)
    3. Giai bai toan
    4. In ket qua ra console
    5. Chay GUI hien thi loi giai
    """
    # TODO: Implement main

    # Buoc 1: Doc ban do
    # map_file = "maps/example_map.txt"
    # game_map = GameMap(map_file)

    # Buoc 2: Tao state ban dau
    # initial_state = State(game_map.agent_pos, game_map.boxes)

    # Buoc 3: Cho user chon thuat toan
    # print("Chon thuat toan:")
    # print("1. UCS")
    # print("2. A*")
    # choice = input("Nhap lua chon (1/2): ")

    # Buoc 4: Giai bai toan
    # if choice == "1":
    #     solver = Solver(game_map)
    #     actions, cost = solver.solve_ucs(initial_state)
    # else:
    #     solver = Solver(game_map, heuristic_func=lambda s: calculate_heuristic(s, game_map))
    #     actions, cost = solver.solve_astar(initial_state)

    # Buoc 5: In ket qua
    # print(f"Actions: {actions}")
    # print(f"Total cost: {cost}")
    # print(f"Nodes expanded: {solver.nodes_expanded}")

    # Buoc 6: Tao list cac states de GUI hien thi
    # states = generate_state_sequence(initial_state, actions, game_map)

    # Buoc 7: Chay GUI
    # gui = GameGUI(game_map, actions, states)
    # gui.run()

    pass


def generate_state_sequence(initial_state, actions, game_map):
    """
    Tu state ban dau va list actions, tao list cac state theo tung buoc.

    Dung cho GUI: hien thi trang thai tai moi buoc, va cho phep di lui.

    Args:
        initial_state: State ban dau
        actions: list cac hanh dong
        game_map: doi tuong GameMap

    Returns:
        list of State: [state_0, state_1, state_2, ..., state_n]
    """
    # TODO: Implement
    # states = [initial_state]
    # current = initial_state
    # for action in actions:
    #     successors = current.get_successors(game_map)
    #     for name, next_state, cost in successors:
    #         if name == action:
    #             states.append(next_state)
    #             current = next_state
    #             break
    # return states
    pass


if __name__ == "__main__":
    main()
