# Giải Thích Thuật Toán & Kiến Thức Cần Biết — Sokoban AI

> File này dùng để ôn tập trước khi vấn đáp. Mỗi thành viên **phải đọc kỹ toàn bộ**,
> không chỉ phần mình phụ trách.

---

## Mục Lục

1. [Mô hình hóa bài toán (Req 1)](#1-mô-hình-hóa-bài-toán-req-1)
2. [Thuật toán UCS (Req 2)](#2-thuật-toán-ucs---uniform-cost-search-req-2)
3. [Thuật toán A* (Req 2)](#3-thuật-toán-a-req-2)
4. [Hàm Heuristic đề xuất (Req 2 & 4)](#4-hàm-heuristic-đề-xuất-req-2--4)
5. [So sánh UCS vs A* (Req 3)](#5-so-sánh-ucs-vs-a-req-3)
6. [Tính Admissible & Consistent (Req 4)](#6-tính-admissible--consistent-req-4)
7. [Deadlock Detection](#7-deadlock-detection)
8. [Chế độ thi đấu 2 Agent (Req 6, 7, 8)](#8-chế-độ-thi-đấu-2-agent-req-6-7-8)
9. [Các thuật toán tìm kiếm khác (BFS, DFS, DLS, IDS, GBFS)](#9-các-thuật-toán-tìm-kiếm-khác)
10. [Câu hỏi vấn đáp thường gặp](#10-câu-hỏi-vấn-đáp-thường-gặp)

---

## 1. Mô Hình Hóa Bài Toán (Req 1)

### Bài toán tìm kiếm không gian trạng thái gồm 5 thành phần:

### 1.1 Trạng thái (State)

Trạng thái = **(vị trí agent, tập vị trí các box)**

```
Ví dụ với bản đồ:
  %%%%%
%%%   %
%DAB  %
%%% BD%
%D%%B %
% % D %%
%B CBBD%
%   D  %
%%%%%%%%

State ban đầu:
  - Agent: (2, 2)       ← tọa độ (hàng, cột) của ký tự 'A'
  - Boxes: {(2,3), (3,4), (4,4), (6,1), (6,4), (6,5), (6,6)}
                         ← vị trí các 'B' và 'C'
```

> **Tại sao không lưu vị trí tường/goal?**  
> Vì tường và goal **không thay đổi** trong suốt game → lưu trong bản đồ, không phải trong state.

### 1.2 Trạng thái ban đầu (Initial State)

- Vị trí ban đầu của agent (ký tự `A`)
- Vị trí ban đầu của tất cả boxes (ký tự `B` và `C`)

### 1.3 Hành động (Actions)

Agent có thể di chuyển 4 hướng: **North, South, East, West**

Quy tắc di chuyển:
```
Trường hợp 1: Ô tiếp theo là ô TRỐNG hoặc GOAL
  → Agent di chuyển bình thường

Trường hợp 2: Ô tiếp theo có BOX
  → Kiểm tra ô phía sau box (cùng hướng di chuyển)
  → Nếu ô đó TRỐNG hoặc GOAL → Agent đẩy box, cả hai cùng di chuyển
  → Nếu ô đó là TƯỜNG hoặc BOX KHÁC → KHÔNG thể di chuyển

Trường hợp 3: Ô tiếp theo là TƯỜNG
  → KHÔNG thể di chuyển
```

### 1.4 Goal Test (Kiểm tra đích)

```
Tất cả vị trí goal (ký tự 'D') đều có box đứng trên → THẮNG
```

Nói cách khác: tập vị trí boxes ⊇ tập vị trí goals

### 1.5 Chi phí (Path Cost)

Mỗi hành động (di chuyển 1 bước) có chi phí = **1**

→ Tổng chi phí = tổng số bước di chuyển

---

## 2. Thuật Toán UCS — Uniform Cost Search (Req 2)

### 2.1 Ý tưởng cốt lõi

UCS mở rộng node có **chi phí đường đi thấp nhất** trước.

> Hãy tưởng tượng bạn đang ở ngã tư. UCS sẽ luôn chọn con đường **ngắn nhất**
> (tính từ điểm xuất phát) để đi tiếp, bất kể hướng nào.

### 2.2 Pseudocode (dễ hiểu)

```
THUẬT TOÁN UCS:
────────────────────────────────────
1.  Tạo hàng đợi ưu tiên (priority queue), gọi là FRONTIER
2.  Đặt state ban đầu vào FRONTIER với chi phí = 0
3.  Tạo tập EXPLORED (các state đã xét) = rỗng

4.  WHILE FRONTIER không rỗng:
5.      Lấy state có CHI PHÍ NHỎ NHẤT ra khỏi FRONTIER → gọi là current
6.      
7.      NẾU current là GOAL STATE:
8.          → Trả về đường đi + tổng chi phí → KẾT THÚC
9.      
10.     Thêm current vào EXPLORED
11.     
12.     VỚI MỖI hành động (North, South, East, West):
13.         Tạo state mới (child) bằng cách thực hiện hành động
14.         chi_phí_mới = chi phí current + 1
15.         
16.         NẾU child CHƯA CÓ trong EXPLORED và CHƯA CÓ trong FRONTIER:
17.             Thêm child vào FRONTIER với chi_phí_mới
18.         HOẶC NẾU child ĐÃ CÓ trong FRONTIER với chi phí CAO HƠN:
19.             Cập nhật chi phí child trong FRONTIER = chi_phí_mới

20. Trả về "Không tìm được lời giải"
────────────────────────────────────
```

### 2.3 Ví dụ minh họa

```
Bản đồ đơn giản:        State ban đầu: Agent=(0,0), Box=(0,1), Goal=(0,3)
A B . D                  
. . . .                  Bước 1: UCS thử 4 hướng → chỉ East hợp lệ (đẩy box)
                         State mới: Agent=(0,1), Box=(0,2), cost=1
                         
                         Bước 2: Từ state cost=1, thử 4 hướng
                         East → Agent=(0,2), Box=(0,3), cost=2 → BOX Ở GOAL → XONG!
                         
                         Kết quả: [East, East], tổng chi phí = 2
```

### 2.4 Tính chất quan trọng

| Tính chất | UCS |
|-----------|-----|
| **Complete** (đầy đủ)? | ✅ Có — luôn tìm được lời giải nếu tồn tại |
| **Optimal** (tối ưu)? | ✅ Có — luôn tìm đường đi ngắn nhất |
| **Thời gian** | O(b^(1+⌊C*/ε⌋)) — chậm vì không có hướng dẫn |
| **Bộ nhớ** | O(b^(1+⌊C*/ε⌋)) — lưu tất cả node đã xét |

> **b** = branching factor (tối đa 4 hướng)  
> **C\*** = chi phí đường đi tối ưu  
> **ε** = chi phí nhỏ nhất mỗi bước (= 1 trong bài này)

---

## 3. Thuật Toán A* (Req 2)

### 3.1 Ý tưởng cốt lõi

A* = UCS + **"trực giác"** (heuristic)

> UCS chỉ nhìn lại (chi phí đã đi). A* nhìn cả **phía trước** (ước tính còn bao xa đến đích).

**Công thức:** f(n) = g(n) + h(n)

```
f(n) = tổng chi phí ước tính
g(n) = chi phí thực tế từ start → n    (giống UCS)
h(n) = chi phí ước tính từ n → goal     (heuristic — "linh cảm")
```

### 3.2 Pseudocode (dễ hiểu)

```
THUẬT TOÁN A*:
────────────────────────────────────
1.  Tạo FRONTIER (priority queue)
2.  Đặt state ban đầu vào FRONTIER với f = 0 + h(start)
3.  Tạo EXPLORED = rỗng

4.  WHILE FRONTIER không rỗng:
5.      Lấy state có f(n) NHỎ NHẤT → gọi là current
6.      
7.      NẾU current là GOAL STATE:
8.          → Trả về đường đi + tổng chi phí → KẾT THÚC
9.      
10.     Thêm current vào EXPLORED
11.     
12.     VỚI MỖI hành động (North, South, East, West):
13.         Tạo child state
14.         g_mới = g(current) + 1
15.         f_mới = g_mới + h(child)           ← KHÁC UCS Ở CHỖ NÀY
16.         
17.         NẾU child CHƯA CÓ trong EXPLORED và CHƯA CÓ trong FRONTIER:
18.             Thêm child vào FRONTIER với f_mới
19.         HOẶC NẾU child ĐÃ CÓ trong FRONTIER với f CAO HƠN:
20.             Cập nhật f của child = f_mới

21. Trả về "Không tìm được lời giải"
────────────────────────────────────
```

### 3.3 So sánh trực quan UCS vs A*

```
         UCS: Tìm kiếm lan tỏa đều mọi hướng (như ném đá xuống ao)
         ●●●●●
        ●●●●●●●
       ●●●S●●●●●        S = Start, G = Goal
        ●●●●●●●          Xét RẤT NHIỀU node vô ích
         ●●●●●

         A*: Tìm kiếm hướng về đích (như la bàn chỉ đường)  
            ●●
           ●●●●
          ●●S●●●          Xét ÍT node hơn nhiều
           ●●●●●●         → Nhanh hơn UCS
              ●●G
```

### 3.4 Tính chất

| Tính chất | A* (với heuristic admissible) |
|-----------|-----|
| **Complete**? | ✅ Có |
| **Optimal**? | ✅ Có — NẾU heuristic admissible |
| **Thời gian** | Tốt hơn UCS (phụ thuộc chất lượng heuristic) |
| **Bộ nhớ** | Vẫn cao — lưu tất cả node trong FRONTIER |

---

## 4. Hàm Heuristic Đề Xuất (Req 2 & 4)

### 4.1 Tại sao không dùng Manhattan/Euclidean?

1. **Đề bài cấm** ❌
2. **Không chính xác**: Manhattan distance bỏ qua tường → có thể cho khoảng cách nhỏ hơn thực tế khi có tường chắn, nhưng quan trọng hơn là nó quá đơn giản, không phản ánh độ khó thực sự của việc đẩy box trong Sokoban

### 4.2 Đề xuất: BFS Distance + Hungarian Algorithm

**Bước 1: Tính khoảng cách BFS giữa mỗi box và mỗi goal**

```
Thay vì dùng Manhattan (đường chim bay):
  Manhattan(box, goal) = |x1-x2| + |y1-y2|     ← BỎ QUA TƯỜNG

Ta dùng BFS (đường đi thực tế):
  BFS_distance(box, goal) = số bước ngắn nhất   ← CÓ TÍNH TƯỜNG
                             đi từ box đến goal
                             trên bản đồ thực tế
```

**Bước 2: Hungarian Algorithm — Ghép nối tối ưu**

```
Ví dụ: 3 boxes (B1, B2, B3) và 3 goals (G1, G2, G3)

Ma trận khoảng cách BFS:
          G1    G2    G3
    B1  [ 3     5     7  ]
    B2  [ 4     2     6  ]
    B3  [ 8     3     1  ]

Hungarian Algorithm tìm cách ghép nối 1-1 sao cho TỔNG nhỏ nhất:
    B1 → G1 (3)
    B2 → G2 (2)       ← Tổng = 3 + 2 + 1 = 6
    B3 → G3 (1)

→ h(state) = 6
```

**Tại sao dùng Hungarian thay vì ghép bừa?**

```
Ghép bừa (ví dụ: B1→G3, B2→G1, B3→G2):
    7 + 4 + 3 = 14    ← Overestimate! Không admissible!

Hungarian luôn cho kết quả NHỎ NHẤT:
    3 + 2 + 1 = 6     ← Không overestimate → Admissible ✅
```

### 4.3 Pseudocode tính Heuristic

```
HÀM calculate_heuristic(state, game_map):
────────────────────────────────────
1.  boxes = danh sách vị trí boxes chưa ở goal
2.  goals = danh sách vị trí goals chưa có box

3.  NẾU không còn box nào chưa ở goal:
4.      return 0     ← Đã đạt mục tiêu

5.  Tạo ma trận cost[i][j]:
6.      VỚI MỖI box_i trong boxes:
7.          VỚI MỖI goal_j trong goals:
8.              cost[i][j] = BFS_shortest_path(box_i, goal_j, game_map)

9.  Áp dụng Hungarian Algorithm trên ma trận cost
10. return tổng chi phí ghép nối tối ưu
────────────────────────────────────
```

---

## 5. So Sánh UCS vs A* (Req 3)

### 5.1 Cách thiết kế thí nghiệm

```
Chạy cả UCS và A* trên CÙNG bản đồ, đo:
  - Thời gian chạy (giây)
  - Số node đã mở rộng (expanded)
  - Số node trong frontier (peak memory)
  - Tổng chi phí đường đi (phải BẰNG NHAU)
```

### 5.2 Bảng kết quả mẫu (cần tự chạy thực tế)

| Metric | UCS | A* |
|--------|-----|----|
| Thời gian | Chậm hơn | Nhanh hơn |
| Nodes expanded | Nhiều hơn | Ít hơn |
| Peak frontier size | Lớn hơn | Nhỏ hơn |
| Solution cost | C* | C* (bằng nhau) |

### 5.3 Giải thích kết quả

```
UCS mở rộng node theo hình tròn (mọi hướng đều nhau)
  → Xét nhiều node không cần thiết
  → Tốn thời gian + bộ nhớ

A* mở rộng node hướng về goal (nhờ heuristic)
  → Xét ít node hơn
  → Nhanh hơn + tiết kiệm bộ nhớ
  → NHƯNG tổng chi phí đường đi vẫn BẰNG UCS (vì cả hai đều optimal)
```

---

## 6. Tính Admissible & Consistent (Req 4)

### 6.1 Admissible (Chấp nhận được)

```
ĐỊNH NGHĨA: h(n) ≤ h*(n) cho MỌI state n

Trong đó:
  h(n)  = giá trị heuristic ta tính
  h*(n) = chi phí THỰC SỰ tối ưu từ n đến goal

NÓI ĐƠN GIẢN: Heuristic KHÔNG BAO GIỜ ước tính QUÁ CAO
```

**Chứng minh heuristic của ta admissible:**

```
1. BFS_distance(box, goal) ≤ chi phí thực tế đẩy box đến goal
   → Vì BFS tính đường đi ngắn nhất cho box, 
     nhưng thực tế agent còn phải đi vòng để đẩy đúng hướng
   → Nên khoảng cách BFS ≤ chi phí thực tế

2. Hungarian Algorithm tìm ghép nối có TỔNG NHỎ NHẤT
   → Tổng nhỏ nhất ≤ bất kỳ cách ghép nối nào khác
   → Bao gồm cả cách ghép nối trong lời giải thực tế

3. Kết hợp: h(n) = Hungarian(BFS distances) ≤ chi phí thực tế ✅
```

### 6.2 Consistent (Nhất quán)

```
ĐỊNH NGHĨA: h(n) ≤ c(n, n') + h(n') cho MỌI cặp state kề (n, n')

Trong đó:
  c(n, n') = chi phí đi từ n sang n' (= 1 trong bài này)
  h(n')    = heuristic tại state n'

NÓI ĐƠN GIẢN: Khi di chuyển 1 bước, heuristic giảm TỐI ĐA bằng chi phí bước đó
```

**Chứng minh consistent:**

```
Khi agent thực hiện 1 hành động (chi phí = 1):
  
  Trường hợp 1: Agent di chuyển KHÔNG đẩy box
    → Vị trí boxes KHÔNG ĐỔI → h(n') = h(n)
    → h(n) - h(n') = 0 ≤ 1 = c(n, n') ✅

  Trường hợp 2: Agent đẩy 1 box
    → Box di chuyển 1 ô → khoảng cách BFS thay đổi tối đa 1
    → Hungarian có thể thay đổi tối đa 1
    → h(n) - h(n') ≤ 1 = c(n, n') ✅
```

### 6.3 Cách kiểm chứng bằng thí nghiệm

```
KIỂM CHỨNG ADMISSIBLE:
────────────────────────────────────
1. Chạy UCS → được chi phí tối ưu h*(start)
2. Với MỖI state n đã xét trong quá trình UCS:
   - Tính h(n) bằng heuristic
   - Tính h*(n) = h*(start) - g(n)    ← vì g(n) + h*(n) = h*(start)
   - Kiểm tra: h(n) ≤ h*(n)
3. Nếu TẤT CẢ đều thỏa → Admissible ✅

KIỂM CHỨNG CONSISTENT:
────────────────────────────────────
1. Trong quá trình A*, với mỗi cặp (parent, child):
   - Tính h(parent), h(child), c(parent, child) = 1
   - Kiểm tra: h(parent) ≤ 1 + h(child)
   - Tức là: h(parent) - h(child) ≤ 1
2. Nếu TẤT CẢ đều thỏa → Consistent ✅
```

---

## 7. Deadlock Detection

### 7.1 Deadlock là gì?

```
Deadlock = trạng thái mà box KHÔNG THỂ đẩy đến goal
         = game CHẮC CHẮN thua → nên bỏ qua state này

Ví dụ:
  %%%
  %B%     ← Box kẹt góc, không thể đẩy đi đâu
  %%%        Nếu góc đó không phải goal → DEADLOCK
```

### 7.2 Các loại Deadlock phổ biến

```
Loại 1: CORNER DEADLOCK (kẹt góc)
  %%          %%
  %B    hoặc  B%    ← Box cạnh 2 tường vuông góc
  
  Phát hiện: Nếu box có 2 mặt bị chặn bởi tường (1 ngang + 1 dọc)
             và vị trí đó KHÔNG phải goal → DEADLOCK

Loại 2: EDGE DEADLOCK (kẹt cạnh)
  %%%%%%%%
  %B     %     ← Box dọc theo tường, không có goal trên cạnh đó
  %%%%%%%%        Không thể đẩy ra khỏi cạnh

  Phát hiện: Nếu box dọc theo tường và không có goal nào trên cạnh đó

Loại 3: FREEZE DEADLOCK (đóng băng)
  %BB%        ← 2 boxes chặn nhau, không box nào di chuyển được
```

### 7.3 Tại sao cần Deadlock Detection?

```
Nếu KHÔNG phát hiện deadlock:
  → A* vẫn tìm kiếm những state vô vọng
  → Tốn thời gian + bộ nhớ vô ích

Nếu CÓ phát hiện deadlock:
  → Cắt bỏ nhánh tìm kiếm vô ích (pruning)
  → A* nhanh hơn ĐÁNG KỂ
```

---

## 8. Chế Độ Thi Đấu 2 Agent (Req 6, 7, 8)

### 8.1 Mô hình hóa (Req 6)

```
KHÁC BIỆT so với single-player:
────────────────────────────────────
1. Có 2 AGENT (thay vì 1)
2. Mỗi agent CÓ MÀU RIÊNG cho boxes của mình
3. Hai agent HÀNH ĐỘNG ĐỒNG THỜI (simultaneous)
4. Giới hạn n bước (do user nhập)
5. Sau n bước: agent nào đặt NHIỀU box vào goal hơn → THẮNG
6. Agent có thể ĐẨY box đã đặt bởi đối thủ RA KHỎI goal
7. Hai agent KHÔNG ĐI XUYÊN qua nhau

STATE MỞ RỘNG:
  (vị_trí_agent_1, vị_trí_agent_2, 
   boxes_của_agent_1, boxes_của_agent_2,
   bước_hiện_tại)
```

### 8.2 Thiết kế thuật toán Agent (Req 7)

```
CHIẾN LƯỢC ĐỀ XUẤT: Greedy A* với đánh giá lại mỗi bước
────────────────────────────────────
MỖI BƯỚC (giới hạn 1000ms):
  1. Tìm goal GẦN NHẤT chưa có box (hoặc có box của đối thủ)
  2. Tìm box GẦN NHẤT có thể đẩy đến goal đó
  3. Dùng A* tìm đường từ agent đến vị trí đẩy box
  4. Thực hiện bước tiếp theo trên đường đi
  5. Nếu phát hiện đối thủ chặn → tìm đường thay thế

TẠI SAO KHÔNG DÙNG MINIMAX?
  → State space quá lớn cho Sokoban
  → Giới hạn 1000ms không đủ để tìm kiếm sâu
  → Greedy A* đủ tốt và nhanh
```

### 8.3 Xử lý di chuyển đồng thời

```
Mỗi game step:
  1. Agent 1 chọn action (dùng thuật toán)    ← ĐỒNG THỜI
     Agent 2 chọn action (dùng thuật toán)    ← ĐỒNG THỜI
  
  2. Kiểm tra xung đột:
     - Nếu 2 agent di chuyển vào CÙNG Ô → cả hai ĐỨNG YÊN
     - Nếu 2 agent đẩy CÙNG box → ưu tiên agent nào? (tự quy định)
  
  3. Thực hiện actions hợp lệ
  4. Cập nhật điểm số
```

---

## 9. Các Thuật Toán Tìm Kiếm Khác

> Những thuật toán này có thể dùng cho Req 7 (agent thi đấu) hoặc GV hỏi vấn đáp.

### 9.1 BFS — Breadth-First Search (Tìm kiếm theo chiều rộng)

```
Ý TƯỞNG: Xét TẤT CẢ node cùng mức trước khi xuống mức tiếp

HÌNH DUNG: Như sóng nước lan tỏa từ 1 điểm

         Mức 0:    S
                  / \
         Mức 1:  A   B        ← Xét A, B trước
                /|    |\
         Mức 2: C D   E F    ← Rồi mới xét C, D, E, F

CẤU TRÚC DỮ LIỆU: Queue (FIFO — vào trước ra trước)

ƯU ĐIỂM: Tìm đường ngắn nhất (khi mọi bước có chi phí bằng nhau)
NHƯỢC ĐIỂM: Tốn nhiều bộ nhớ (lưu toàn bộ mức hiện tại)
```

```
PSEUDOCODE BFS:
────────────────────────────────
1. Tạo QUEUE, đặt start vào
2. Tạo EXPLORED = rỗng

3. WHILE QUEUE không rỗng:
4.   Lấy node ĐẦU TIÊN ra → current
5.   NẾU current = GOAL → trả về đường đi
6.   Thêm current vào EXPLORED
7.   VỚI MỖI child của current:
8.     NẾU child chưa trong EXPLORED và QUEUE:
9.       Thêm child vào CUỐI QUEUE
────────────────────────────────
```

### 9.2 DFS — Depth-First Search (Tìm kiếm theo chiều sâu)

```
Ý TƯỞNG: Đi SÂU nhất có thể, quay lại khi bí

HÌNH DUNG: Như đi trong mê cung, luôn rẽ trái
           đến khi bí → quay lại → rẽ hướng khác

         S
        /
       A
      /
     C ← đi sâu xuống hết
    / 
   ...

CẤU TRÚC DỮ LIỆU: Stack (LIFO — vào sau ra trước) hoặc đệ quy

ƯU ĐIỂM: Ít tốn bộ nhớ (chỉ lưu đường đi hiện tại)
NHƯỢC ĐIỂM: Không đảm bảo tìm đường ngắn nhất
            Có thể lặp vô hạn nếu không kiểm tra
```

### 9.3 DLS — Depth-Limited Search (Tìm kiếm giới hạn độ sâu)

```
Ý TƯỞNG: DFS nhưng giới hạn độ sâu tối đa = L

  NẾU depth > L → dừng, không đi sâu thêm
  → Tránh vấn đề lặp vô hạn của DFS

VÍ DỤ: DLS với L = 3
        S (depth 0)
       /
      A (depth 1)
     /
    C (depth 2)
   /
  D (depth 3) ← DỪNG, không đi tiếp
```

### 9.4 IDS — Iterative Deepening Search (Tìm kiếm sâu dần)

```
Ý TƯỞNG: Chạy DLS nhiều lần, tăng L mỗi lần

  Lần 1: DLS với L = 0
  Lần 2: DLS với L = 1
  Lần 3: DLS với L = 2
  ...cho đến khi tìm được goal

TẠI SAO HAY?
  → Kết hợp ưu điểm BFS (tìm đường ngắn nhất)
    với ưu điểm DFS (ít tốn bộ nhớ)
  → Tuy chạy lại nhiều lần nhưng overhead nhỏ
```

### 9.5 GBFS — Greedy Best-First Search (Tìm kiếm tham lam)

```
Ý TƯỞNG: Luôn chọn node "TRÔNG CÓ VẺ" gần goal nhất

  Dùng f(n) = h(n)     ← CHỈ dùng heuristic, KHÔNG có g(n)

SO SÁNH:
  UCS:  f(n) = g(n)           ← chỉ nhìn quá khứ
  GBFS: f(n) = h(n)           ← chỉ nhìn tương lai
  A*:   f(n) = g(n) + h(n)    ← nhìn cả hai

ƯU ĐIỂM: Rất nhanh
NHƯỢC ĐIỂM: KHÔNG đảm bảo tối ưu (có thể tìm đường dài hơn)
```

### 9.6 Bảng tổng hợp so sánh

| Thuật toán | Complete | Optimal | Thời gian | Bộ nhớ | Cấu trúc |
|------------|:--------:|:-------:|:---------:|:------:|:---------:|
| **BFS** | ✅ | ✅* | O(b^d) | O(b^d) | Queue |
| **DFS** | ❌** | ❌ | O(b^m) | O(bm) | Stack |
| **DLS** | ❌ | ❌ | O(b^L) | O(bL) | Stack |
| **IDS** | ✅ | ✅* | O(b^d) | O(bd) | Stack |
| **UCS** | ✅ | ✅ | O(b^(1+⌊C*/ε⌋)) | O(b^(1+⌊C*/ε⌋)) | PQ |
| **GBFS** | ❌ | ❌ | O(b^m) | O(b^m) | PQ |
| **A*** | ✅ | ✅*** | O(b^d) | O(b^d) | PQ |

> \* khi chi phí mỗi bước bằng nhau  
> \*\* có thể bị vòng lặp vô hạn  
> \*\*\* khi heuristic admissible  
> b = branching factor, d = depth of solution, m = max depth, L = limit

---

## 10. Câu Hỏi Vấn Đáp Thường Gặp

### ❓ Nhóm câu hỏi về BÀI TOÁN:

**Q: State space của Sokoban bao lớn?**
> Nếu bản đồ có N ô trống và M boxes:
> Số state = N × C(N-1, M) = N × (N-1)! / (M! × (N-1-M)!)
> Rất lớn! Ví dụ: 30 ô trống, 7 boxes → hàng triệu states

**Q: Tại sao Sokoban khó?**
> Sokoban đã được chứng minh là NP-hard (thậm chí PSPACE-complete).
> Lý do: Box chỉ đẩy được (không kéo), và có thể tạo deadlock.

**Q: Branching factor thực tế bao nhiêu?**
> Tối đa 4 (N, S, E, W), nhưng thực tế thường 2-3 do tường và box chặn.

---

### ❓ Nhóm câu hỏi về THUẬT TOÁN:

**Q: UCS và A* khác nhau chỗ nào?**
> Chỉ khác ở priority trong queue:
> - UCS: priority = g(n) (chi phí đã đi)
> - A*: priority = g(n) + h(n) (chi phí đã đi + ước tính còn lại)

**Q: Nếu h(n) = 0 cho mọi n, A* thành thuật toán gì?**
> A* thành UCS. Vì f(n) = g(n) + 0 = g(n).

**Q: Heuristic tốt hơn nghĩa là gì?**
> h1 tốt hơn h2 nếu h1(n) ≥ h2(n) cho mọi n (và cả hai đều admissible).
> → h1 dominate h2 → A* với h1 mở rộng ít node hơn.

**Q: Tại sao không dùng DFS cho Sokoban?**
> DFS không optimal và có thể bị loop vô hạn. Sokoban cần tìm đường ngắn nhất.

---

### ❓ Nhóm câu hỏi về HEURISTIC:

**Q: Admissible là gì? Consistent là gì?**
> Admissible: h(n) ≤ h*(n) — không bao giờ ước tính quá cao
> Consistent: h(n) ≤ c(n,n') + h(n') — giảm tối đa bằng chi phí mỗi bước
> Consistent → Admissible (nhưng ngược lại chưa chắc)

**Q: Nếu heuristic KHÔNG admissible thì sao?**
> A* có thể tìm được lời giải KHÔNG tối ưu (đường đi dài hơn cần thiết).

**Q: Tại sao dùng Hungarian algorithm?**
> Vì bài toán ghép nối box-goal là bài toán **assignment problem**.
> Hungarian giải tối ưu trong O(n³), cho kết quả nhỏ nhất → admissible.

---

### ❓ Nhóm câu hỏi về COMPETITIVE MODE:

**Q: Xử lý xung đột giữa 2 agent thế nào?**
> Nếu cả hai muốn vào cùng ô → cả hai đứng yên (hoặc theo quy tắc ta định nghĩa).

**Q: Agent biết vị trí đối thủ không?**
> Có — full observable. Agent thấy toàn bộ bản đồ mỗi bước.

**Q: Tại sao dùng Greedy thay vì Minimax?**
> Minimax yêu cầu duyệt cây game rất sâu — quá chậm cho Sokoban (PSPACE-complete).
> Greedy A* đủ tốt trong thời hạn 1000ms mỗi bước.

---

### ❓ Nhóm câu hỏi về CODE:

**Q: Tại sao dùng OOP?**
> Đề bài yêu cầu. Tách biệt responsibilities:
> GameMap lo đọc bản đồ, State lo trạng thái, Solver lo thuật toán, GUI lo hiển thị.

**Q: Làm sao lưu state hiệu quả?**
> Dùng tuple (vị trí agent, frozenset vị trí boxes) → hashable → dùng trong set/dict.

**Q: Tại sao dùng frozenset cho boxes?**
> Set thường KHÔNG hashable → không dùng trong set EXPLORED được.
> Frozenset là immutable → hashable → dùng được.

---

> **Lời khuyên vấn đáp:**
> 1. Trả lời ngắn gọn, đi thẳng vào vấn đề
> 2. Nếu không biết → nói "Em không chắc" → tốt hơn nói bừa
> 3. Vẽ hình nếu cần giải thích (mang bút)
> 4. Hiểu WHY quan trọng hơn HOW — giảng viên thường hỏi "tại sao" chứ không "code thế nào"
