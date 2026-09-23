# Huong Dan Chi Tiet — Thanh Vien C
# (Req 6, Req 8, Task 2: Slide + Video)

## Tong quan cong viec cua ban

- Req 6: Mo hinh hoa bai toan 2-agent thi dau (VIET TAI LIEU)
- Req 8: Mo rong GUI cho che do thi dau (CODE dua tren gui.py cua A)
- Task 2: Lam slide thuyet trinh + quay video demo

---

## Req 6: Mo hinh hoa 2-agent (1.0 diem)

### Luat choi thi dau

```
1. Hai agent CUNG thi dau tren 1 ban do
2. Moi luot, ca 2 DONG THOI chon hanh dong
3. Gioi han n buoc (user nhap n truoc khi bat dau)
4. Sau n buoc: agent nao dat NHIEU box vao goal hon -> THANG
5. Agent co the DAY box cua doi thu RA KHOI goal
6. Hai agent KHONG DI XUYEN qua nhau
```

### Mo hinh hoa (tuong tu Req 1 nhung cho 2 agent)

```
STATE:
  (pos_agent1, pos_agent2, boxes, box_ownership, step)
  
  - pos_agent1: vi tri agent 1
  - pos_agent2: vi tri agent 2
  - boxes: tap vi tri tat ca boxes
  - box_ownership: dict {box_pos: agent_id}
    (box thuoc agent nao, hoac None neu chua ai dat)
  - step: buoc hien tai (0 -> n)

ACTIONS:
  Moi agent co 5 lua chon: North, South, East, West, Stay
  -> Tong hop: (action_agent1, action_agent2) = 5 x 5 = 25 to hop

TRANSITION:
  1. Ca 2 agent chon action dong thoi
  2. Kiem tra xung dot:
     - 2 agent vao cung o -> ca 2 dung yen
     - 2 agent di xuyen qua nhau (swap) -> ca 2 dung yen
  3. Thuc hien action hop le
  4. Cap nhat box_ownership khi agent day box vao goal

GOAL TEST:
  Khong co "thang tuyet doi" — chi so sanh diem sau n buoc

SCORING:
  Dem so box cua moi agent dang o vi tri goal
  Agent co nhieu hon -> thang
```

### Thiet ke ban do thi dau

```
Yeu cau:
- LON HON ban do single-player (de 2 agent co khong gian)
- DOI XUNG (cong bang cho 2 agent)
- Nhieu goal va box (de ca 2 deu co co hoi)

Da co san file: source/task1_competitive/maps/competitive_map.txt
Ban co the chinh sua hoac tao ban do moi
```

---

## Req 8: GUI thi dau (1.0 diem)

### Dua tren gui.py cua thanh vien A, them:

```
1. HIEN THI 2 AGENT:
   - Agent 1: mau XANH DUONG
   - Agent 2: mau DO CAM

2. BOX CO MAU KHAC NHAU:
   - Box cua agent 1: mau xanh nhat
   - Box cua agent 2: mau cam
   - Box chua ai dat: mau nau mac dinh

3. PANEL THONG TIN:
   - Diem agent 1: X
   - Diem agent 2: Y
   - Buoc con lai: Z
   - Trang thai: Dang chay / Ket thuc

4. KET QUA:
   - Khi het n buoc, hien thi: "Agent 1 THANG!" hoac "HOA"
```

### Cac buoc thuc hien:

```
Buoc 1: Copy gui.py tu task1, doi ten thanh competitive_gui.py
Buoc 2: Them agent 2 vao draw()
Buoc 3: Them mau sac cho box theo ownership
Buoc 4: Sua panel thong tin (them diem, buoc con lai)
Buoc 5: Them man hinh ket qua
Buoc 6: Tich hop agent_algorithm.py (goi choose_action moi buoc)
```

---

## Task 2: Slide thuyet trinh (2.0 diem)

### Yeu cau format:
- Ti le slide 4:3
- KHONG dung nen toi
- KHONG dung hinh mau sac ruc ro (may chieu khong hien thi tot)
- NOI DUNG phai doc duoc khi in trang den
- Thoi luong: TOI DA 5 phut

### Cau truc slide:

```
Slide 1: Trang bia
  - Ten truong, khoa, mon hoc
  - Ten de tai: "Sokoban - Search Algorithms"
  - Danh sach nhom

Slide 2: Danh sach thanh vien
  - MSSV, ho ten, email
  - Nhiem vu duoc giao
  - % hoan thanh

Slide 3-4: Mo hinh hoa bai toan (Req 1)
  - State, Action, Goal Test, Cost
  - Dung so do / hinh ve minh hoa

Slide 5-6: Thuat toan UCS va A* (Req 2)
  - Pseudocode (KHONG copy source code!)
  - So do flowchart hoac hinh minh hoa

Slide 7: Heuristic (Req 2)
  - Giai thich BFS + Hungarian
  - Vi du nho minh hoa

Slide 8: Ket qua thi nghiem (Req 3)
  - Bang so sanh UCS vs A*
  - Bieu do (neu co)

Slide 9: Kiem chung heuristic (Req 4)
  - Dinh nghia admissible/consistent
  - Ket qua kiem chung

Slide 10: GUI demo (Req 5)
  - Screenshot game
  - Cac chuc nang: pause, forward, backward

Slide 11-12: Che do thi dau (Req 6, 7, 8)
  - Mo hinh 2-agent
  - Chien luoc agent
  - Screenshot GUI thi dau

Slide 13: Bang hoan thanh
  | Req | Noi dung | % hoan thanh |
  |-----|----------|-------------|
  | 1   | ...      | 100%        |

Slide 14: Uu nhuoc diem
  - Uu: A* nhanh, heuristic tot, GUI de dung
  - Nhuoc: Chua xu ly deadlock phuc tap, ...
```

### Video demo (toi da 3 phut):
```
1. Chay single-player voi UCS (30 giay)
2. Chay single-player voi A* (30 giay)
3. So sanh ket qua (20 giay)
4. Chay competitive mode (60 giay)
5. Ket qua thi dau (20 giay)
```

---

## Cau hoi van dap ban can chuan bi

1. "Che do thi dau khac gi single-player?" -> 2 agent, dong thoi, gioi han n buoc
2. "Xu ly xung dot the nao?" -> Ca 2 dung yen neu vao cung o
3. "Box ownership hoat dong the nao?" -> Agent nao day box vao goal -> box cua agent do
4. "GUI thi dau khac gi GUI thuong?" -> 2 mau agent, mau box khac nhau, hien diem
5. "Slide co gi?" -> Tong ket cac slide nhu tren
