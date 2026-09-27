# Dependencies
import heapq
from collections import deque
import itertools
import numpy as np

def load_map(filepath):
    walls = set()
    boxes = set()
    goal = set()
    agent = None

    with open(filepath, 'r') as f:
        for r, line in enumerate(f):
            for c, char in enumerate(line.strip('\n')):
                pos = (r,c)
                if char == "#":
                    walls.add(pos)
                elif char == "B":
                    boxes.add(pos)
                elif char == "C":
                    goal.add(pos)
                    boxes.add(pos)
                elif char == "D":
                    goal.add(pos)
                elif char == "A":
                    agent = pos

    initial_state = (agent, frozenset(boxes))
    return initial_state, walls, goal

def is_goal(state, goal):
    agent_pos, boxes = state
    return boxes == goal

def get_successors(state, walls):
    successor = []
    agent_pos, boxes = state
    r, c = agent_pos

    Direction = [(-1,0), (1,0), (0,-1), (0,1)]

    for d_r, d_c in Direction:
        new_r = r + d_r
        new_c = c + d_c
        new_agent_pos = (new_r, new_c)

        if new_agent_pos in walls:
            continue
        if new_agent_pos in boxes:
            new_box_r = new_r + d_r
            new_box_c = new_c + d_c
            new_boxe_pos = (new_box_r, new_box_c)

            if new_boxe_pos in boxes or new_boxe_pos in walls:
                continue


            new_box = set(boxes)
            new_box.remove(new_agent_pos)
            new_box.add(new_boxe_pos)

            next_state = (new_agent_pos, frozenset(new_box))
            successor.append(next_state)
        else:
            next_state = (new_agent_pos, frozenset(boxes))
            successor.append(next_state)
    return successor

def get_bfs_distance(box_pos, goals, walls):
    queue = deque([(box_pos, 0)]) # Truyen vao box_position va distance hien tai
    explored = {box_pos}
    distance = {}

    while queue:
        curr, dist = queue.popleft()

        if curr in goals:
            distance[curr] = dist
        r, c = curr
        for d_r, d_c in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            next_pos = (r + d_r, c + d_c)

            if next_pos not in walls and next_pos not in explored:
                explored.add(next_pos)
                queue.append((next_pos, dist + 1))
    for g in goals:
        if g not in distance:
            distance[g] = np.inf
    return distance #tra ve mot dictionary co toa do (box va distance)

def heuristic_func(state, goals, walls):
    _, boxes = state
    boxes_list = list(boxes)
    goals_list = list(goals)

    if not boxes_list:
        return 0
    cost_matrix = []
    for b in boxes_list:
        dist_dict = get_bfs_distance(b, goals, walls)
        row = [dist_dict[g] for g in goals_list]
        cost_matrix.append(row)
    n_boxes = len(boxes_list)
    n_goals = len(goals_list)
    
    # 2. Xử lý lỗi nếu bản đồ thiết kế sai (số hộp không bằng số đích)
    if n_boxes != n_goals:
        h = 0
        for b in boxes:
            if b not in goals:
                h += min(abs(b[0] - g[0]) + abs(b[1] - g[1]) for g in goals)
        return h

    # 3. Tìm tổng chi phí nhỏ nhất bằng hoán vị
    min_total_cost = float('inf')
    for p in itertools.permutations(range(n_boxes)):
        current_cost = sum(cost_matrix[r][p[r]] for r in range(n_boxes))
        if current_cost < min_total_cost:
            min_total_cost = current_cost
            
    return min_total_cost

def get_true_cost(start_state, walls, goals):
    counter = itertools.count()
    frontier = []
    heapq.heappush(frontier, (0, next(counter), start_state))
    explored = set()
    
    while frontier:
        g_cost, _, current_state = heapq.heappop(frontier)
        if current_state in explored: 
            continue
        explored.add(current_state)
        
        if is_goal(current_state, goals):
            return g_cost
            
        for next_state in get_successors(current_state, walls):
            if next_state not in explored:
                heapq.heappush(frontier, (g_cost + 1, next(counter), next_state))
                
    return float('inf')

def generate_sample_states(initial_state, walls, max_states=1500):
    """
    Dùng thuật toán BFS để loang ra từ trạng thái đầu, 
    thu thập đủ max_states (ví dụ: 1500 trạng thái) làm dữ liệu test.
    """
    states = [] # Mảng chứa kết quả
    
    # Hàng đợi (queue) và tập hợp (set) đặc trưng của thuật toán BFS
    queue = deque([initial_state])
    explored = set([initial_state])
    
    # Vòng lặp chạy cho đến khi gom đủ 1500 state hoặc không còn đường đi
    while queue and len(states) < max_states:
        current = queue.popleft()
        
        # Cất trạng thái vừa lấy ra vào kho dữ liệu
        states.append(current)
        
        # Thử đi tất cả các bước có thể từ trạng thái hiện tại
        for nxt in get_successors(current, walls):
            if nxt not in explored:
                explored.add(nxt)
                queue.append(nxt)
                
    return states

def verify_heuristic(filepath):
    initial_state, walls, goals = load_map(filepath)
    print(f"Đang trích xuất dữ liệu từ {filepath}...")
    test_states = generate_sample_states(initial_state, walls, 1500)
    
    consistent_violations = 0
    pair_count = 0
    
    for state in test_states:
        h_n = heuristic_func(state, goals, walls)
        
        for nxt_state in get_successors(state, walls):
            h_nxt = heuristic_func(nxt_state, goals, walls)
            pair_count += 1
            
            if h_n - h_nxt > 1:
                consistent_violations += 1

    print("\n=== KIEM CHUNG CONSISTENT ===")
    print(f"Tong so cap kiem tra: {pair_count}")
    print(f"So vi pham: {consistent_violations}")
    print("Ket luan: CONSISTENT ✅" if consistent_violations == 0 else "Ket luan: KHONG CONSISTENT ❌")

    admissible_violations = 0
    state_count = 0
    
    for state in test_states[:50]:
        h_n = heuristic_func(state, goals, walls) 
        h_star_n = get_true_cost(state, walls, goals)
        
        if h_star_n != float('inf'):
            state_count += 1
            if h_n > h_star_n:
                admissible_violations += 1

    print("\n=== KIEM CHUNG ADMISSIBLE ===")
    print(f"Tong so state kiem tra: {state_count}")
    print(f"So vi pham: {admissible_violations}")
    print("Ket luan: ADMISSIBLE ✅" if admissible_violations == 0 else "Ket luan: KHONG ADMISSIBLE ❌")

if __name__ == "__main__":
    print("Đang chạy kiểm chứng... Vui lòng đợi.")
    verify_heuristic("map/ez_map.txt")
    