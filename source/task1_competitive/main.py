# main.py
# Diem khoi chay chinh (Entry point) cho che do thi dau 2 agent

import os
import sys

# Dam bao encoding tren Windows
if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from game_map import CompetitiveGameMap
from competitive_gui import CompetitiveGUI
from agent_algorithm import Agent as Agent1
from agent_opponent import Agent as Agent2


def main():
    map_file = "maps/competitive_map.txt"
    if not os.path.exists(map_file):
        print(f"Loi: Khong tim thay file ban do {map_file}")
        return

    print("=" * 60)
    print("SOKOBAN — CHE DO THI DAU 2 AGENT (Competitive Mode)")
    print("=" * 60)
    print(f"Dang tai ban do: {map_file}")

    game_map = CompetitiveGameMap(map_file)
    print(f"Kich thuoc ban do: {game_map.rows} x {game_map.cols}")
    print(f"Vi tri Agent 1: {game_map.agent1_pos}")
    print(f"Vi tri Agent 2: {game_map.agent2_pos}")
    print(f"So luong hop (boxes): {len(game_map.boxes)}")
    print(f"So luong dich (goals): {len(game_map.goals)}")

    # Nhap so buoc thi dau n
    print("\nHai agent se thi dau trong n buoc.")
    step_input = input("Nhap so buoc thi dau n (Mac dinh: 60): ").strip()
    try:
        step_limit = int(step_input) if step_input else 60
    except ValueError:
        step_limit = 60

    print(f"\n[+] Da thiet lap so buoc thi dau: n = {step_limit}")
    print("[+] Khoi tao Agent 1 (agent_algorithm.py) va Agent 2 (agent_opponent.py)...")

    agent1 = Agent1(agent_id=1)
    agent2 = Agent2(agent_id=2)

    print("[+] Dang khoi dong Giao dien thi dau (Pygame)...")
    print("    Nhan SPACE de Bat dau / Tam dung thi dau.")
    gui = CompetitiveGUI(game_map, agent1, agent2, step_limit=step_limit)
    gui.run()


if __name__ == "__main__":
    main()
