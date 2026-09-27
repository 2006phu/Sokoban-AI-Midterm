#Dependencies
import heapq
import time
import itertools
import os

# Initial Function

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

# Ham thuat toan

def ucs_search(initial_state, walls, goals):
    start_time = time.time()
    counter = itertools.count() # Dùng để xử lý lỗi so sánh frozenset trong heapq
    
    frontier = []
    heapq.heappush(frontier, (0, next(counter), initial_state))
    
    explored = set()
    nodes_expanded = 0
    max_frontier = 0
    
    while frontier:
        if len(frontier) > max_frontier:
            max_frontier = len(frontier)
            
        g_cost, _, current_state = heapq.heappop(frontier)
        
        if current_state in explored:
            continue
            
        explored.add(current_state)
        nodes_expanded += 1
        if is_goal(current_state, goals):
            return {
                "time": time.time() - start_time,
                "nodes": nodes_expanded,
                "max_frontier": max_frontier,
                "cost": g_cost
            }
            
        successors = get_successors(current_state, walls)
        for next_state in successors:
            if next_state not in explored:
                heapq.heappush(frontier, (g_cost + 1, next(counter), next_state))
                
    return None

def a_star_search(initial_state, walls, goals, heuristic_func):
    start_time = time.time()
    counter = itertools.count()
    
    frontier = []
    heapq.heappush(frontier, (0, 0, next(counter), initial_state))
    
    explored = set()
    nodes_expanded = 0
    max_frontier = 0
    
    while frontier:
        if len(frontier) > max_frontier:
            max_frontier = len(frontier)
            
        f_cost, g_cost, _, current_state = heapq.heappop(frontier)
        
        if current_state in explored:
            continue
            
        explored.add(current_state)
        nodes_expanded += 1
        
        if is_goal(current_state, goals):
            return {
                "time": time.time() - start_time,
                "nodes": nodes_expanded,
                "max_frontier": max_frontier,
                "cost": g_cost
            }
            
        successors = get_successors(current_state, walls)
        for next_state in successors:
            if next_state not in explored:
                new_g_cost = g_cost + 1
                h_cost = heuristic_func(next_state, goals) 
                new_f_cost = new_g_cost + h_cost
                heapq.heappush(frontier, (new_f_cost, new_g_cost, next(counter), next_state))
                
    return None

# Chay thi nghiem
def dummy_heuristic(state, goals):
    # Tính khoảng cách Manhattan từ các hộp chưa vào đích đến đích gần nhất
    _, boxes = state
    h = 0
    for b in boxes:
        if b not in goals:
            min_dist = min(abs(b[0] - g[0]) + abs(b[1] - g[1]) for g in goals)
            h += min_dist
    return h

if __name__ == "__main__":
    maps = [
        ("Eazy", "map/ez_map.txt"),
        ("Medium", "map/med_map.txt"),
        ("Hard", "map/hard_map.txt")
    ]

    print(f"{'Bản đồ':<10} | {'Thuật toán':<10} | {'Thời gian (s)':<15} | {'Node mở rộng':<15} | {'Max Frontier':<15} | {'Chi phí':<10}")
    print("-" * 85)

    for map_name, filepath in maps:
        try:
            initial_state, walls, goal = load_map(filepath)
            res_ucs = ucs_search(initial_state, walls, goal)
            if res_ucs:
                print(f"{map_name:<10} | {'UCS':<10} | {res_ucs['time']:<15.4f} | {res_ucs['nodes']:<15} | {res_ucs['max_frontier']:<15} | {res_ucs['cost']:<10}")
            else:
                print(f"{map_name:<10} | {'UCS':<10} | {'Không tìm thấy lời giải':<15}")

            res_astar = a_star_search(initial_state, walls, goal, dummy_heuristic)
            if res_astar:
                print(f"{'':<10} | {'A*':<10} | {res_astar['time']:<15.4f} | {res_astar['nodes']:<15} | {res_astar['max_frontier']:<15} | {res_astar['cost']:<10}")
            else:
                print(f"{'':<10} | {'A*':<10} | {'Không tìm thấy lời giải':<15}")
                



        except FileNotFoundError:
            print(f"LỖI: Không tìm thấy file '{filepath}'. Vui lòng kiểm tra lại tên file và đường dẫn.")
            print("-" * 85)

