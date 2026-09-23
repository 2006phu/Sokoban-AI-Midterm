# Huong Dan Chi Tiet — Thanh Vien B
# (Req 1, Req 3, Req 4)

## Tong quan cong viec cua ban

Ban phu trach 3 requirements, chu yeu la **phan tich** va **thi nghiem**:
- Req 1: Mo hinh hoa bai toan (VIET TAI LIEU)
- Req 3: Thi nghiem so sanh UCS vs A* (CHAY THI NGHIEM)
- Req 4: Kiem chung heuristic (PHAN TICH + CODE DON GIAN)

---

## Req 1: Mo hinh hoa bai toan (1.0 diem)

### Ban can viet gi?

Mot tai lieu (co the la phan cua slide) mo ta bai toan Sokoban
theo **5 thanh phan cua bai toan tim kiem**:

### 1. Tap trang thai (State Space)
```
State = (vi_tri_agent, tap_vi_tri_boxes)

Vi du:
  State = ((2,2), frozenset({(2,3), (3,4), (4,4), (6,1), (6,4), (6,5), (6,6)}))
  
  Trong do:
  - (2,2) = agent o hang 2, cot 2
  - frozenset{...} = vi tri cua 7 boxes
```

### 2. Trang thai ban dau (Initial State)
```
Doc tu file ban do:
- 'A' -> vi tri agent
- 'B' -> vi tri box
- 'C' -> vi tri box (dang o tren goal)
```

### 3. Tap hanh dong (Actions)
```
4 hanh dong: North, South, East, West

Dieu kien:
- O dich khong phai tuong
- Neu o dich co box: o phia sau box (cung huong) phai trong va khong co box khac
```

### 4. Ham chuyen trang thai (Transition Function)
```
Hanh dong -> trang thai moi

Vi du: Agent o (2,2), Box o (2,3)
  Action "East" ->
    Agent moi: (2,3)
    Box moi: (2,4)  (bi day sang phai)
```

### 5. Kiem tra dich (Goal Test)
```
Tat ca vi tri goal (ky tu 'D') deu co box dung tren
```

### 6. Chi phi (Path Cost)
```
Moi hanh dong co chi phi = 1
Tong chi phi = so buoc di chuyen
```

---

## Req 3: Thi nghiem so sanh (1.0 diem)

### Ban can lam gi?

1. **Tao them 2-3 ban do** voi do kho khac nhau (de, trung binh, kho)
   - Ban do de: 2-3 boxes, it tuong
   - Ban do trung binh: 4-5 boxes
   - Ban do kho: 6+ boxes, nhieu tuong

2. **Chay UCS va A*** tren moi ban do

3. **Ghi lai 4 chi so:**
   - Thoi gian chay (giay)
   - So node mo rong
   - Kich thuoc frontier lon nhat
   - Chi phi loi giai

4. **Lap bang so sanh** va **viet nhan xet**

### Mau bang ket qua:
```
| Ban do    | Metric            | UCS      | A*       |
|-----------|-------------------|----------|----------|
| Easy      | Thoi gian (s)     | 0.05     | 0.01     |
|           | Nodes expanded    | 500      | 100      |
|           | Max frontier      | 200      | 50       |
|           | Solution cost     | 15       | 15       |
| Medium    | ...               | ...      | ...      |
| Hard      | ...               | ...      | ...      |
```

### Nhan xet can co:
- A* nhanh hon UCS bao nhieu lan?
- So node A* it hon bao nhieu?
- Chi phi loi giai co BANG NHAU khong? (phai bang)
- Khi do kho tang, chenh lech co tang khong?

---

## Req 4: Kiem chung heuristic (1.0 diem)

### Phan 1: Phan tich ly thuyet

Viet tai lieu giai thich:
1. **Heuristic cua nhom la gi?**
   → BFS Distance + Hungarian Algorithm

2. **Tai sao admissible?**
   → Vi BFS distance <= chi phi thuc day box
   → Hungarian cho tong nho nhat -> khong overestimate

3. **Tai sao consistent?**
   → Moi buoc chi day 1 box, di 1 o
   → h(n) giam toi da 1 = chi phi buoc do

### Phan 2: Kiem chung thuc nghiem

Chay script `heuristic_verification.py`:
1. Kiem tra h(n) <= h*(n) cho nhieu state
2. Kiem tra h(n) - h(n') <= 1 cho moi cap ke
3. Bao cao: bao nhieu state da kiem tra, co vi pham khong

### Ket qua mong doi:
```
=== KIEM CHUNG ADMISSIBLE ===
Tong so state kiem tra: 1500
So vi pham: 0
Ket luan: ADMISSIBLE ✅

=== KIEM CHUNG CONSISTENT ===
Tong so cap kiem tra: 3000
So vi pham: 0
Ket luan: CONSISTENT ✅
```

---

## Cau hoi van dap ban can chuan bi

1. "State space la gi?" -> Tra loi theo muc 1 o tren
2. "Chi phi moi buoc la bao nhieu?" -> 1
3. "UCS va A* khac gi?" -> Priority: g(n) vs g(n)+h(n)
4. "Heuristic cua nhom la gi?" -> BFS + Hungarian
5. "Tai sao admissible?" -> Xem phan tich o tren
6. "A* co luon tot hon UCS khong?" -> Co, khi heuristic tot. Cung cost nhung it node hon.
