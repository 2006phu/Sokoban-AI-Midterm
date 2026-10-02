## Thanh vien C - Slide va video demo

Storyboard cho phan trinh bay cua nhom. Dat ti le slide 4:3, nen sang, su dung mau chu dao theo template bai giang (Dark Green #4B7E1B), noi dung hoc thuat 100% tieng Anh va dam bao thoi luong trinh bay duoi 05 phut.

### Noi dung 7 slide bao cao (Execution-Focused)

1. **Title Slide (Trang bia):** Thong tin Truong Dai hoc Ton Duc Thang, khoa CNTT, mon Nhap mon Tri tue Nhan tao (503043), de tai *Sokoban AI Solver & Two-Agent Battle*, nhom 08 va GVHD ThS. Nguyen Thanh An.
2. **Team Members & Task Allocation:** Bang phan cong chi tiet MSSV, ho ten, email hoc thuat, phan cong nhiem vu (Phu: Req 2, 5, 7; Huy: Req 1, 3, 4; Khoi: Req 6, 8, Task 2) va tien do hoan thanh 100%.
3. **Problem Formulation & Heuristic Design:** Mo hinh hoa khong gian trang thai don (Agent, Boxes, Actions, Transition, Goal Test) va ma gia ham Heuristic (BFS tinh nguoc tu Goal ket hop Hungarian matching/bipartite graph) kem chung minh Admissibility & Consistency.
4. **A\* Search Implementation:** Ma gia thuat toan A\* Graph Search chuan form giao trinh, tich hop hang doi uu tien f(n) = g(n) + h(n) va co che cat tia goc chet (Deadlock Pruning).
5. **Empirical Evaluation (UCS vs. A\*):** Bang ket qua thuc nghiem tren 4 cap do ban do (Easy, Medium, Hard, Sample); doi sanh chi phi toi uu, do giam so node mo rong (giam toi 6.2x) va thoi gian thuc thi.
6. **Competitive Two-Agent Engine & Decision Strategy:** Mo hinh doi khang 2 agent (hanh dong dong thoi, xu ly va cham, luat cuop hop va gioi han thoi gian <= 1000ms) kem ma gia bo dieu phoi hanh dong (Opportunistic Stealing + Greedy Goal Delivery + Alpha-Beta Search).
7. **System Evaluation & Project Deliverables:** Uu/nhuoc diem cua giai phap, bang nghiem thu hoan thanh 100% cac yeu cau tu Req 1 den Req 8, link repository GitHub va thong tin video demo trong demo.txt (<= 03 phut).

## Kich ban video toi da 3 phut

- 0:00-0:30: chay single-player voi UCS.
- 0:30-1:00: chay single-player voi A*.
- 1:00-1:20: cho thay bang so sanh ket qua.
- 1:20-2:20: chay competitive, nhap so buoc, cho thay hai agent va diem cap nhat.
- 2:20-2:40: cho thay xu ly xung dot va mau box.
- 2:40-3:00: ket qua thang/thua/hoa va ket luan.

## Phan can xac nhan truoc khi chot slide/video

- Chay ban competitive hien tai va xac nhan ca `agent_algorithm.py` va `agent_opponent.py` hoat dong; khong dung ban cu chi tra `Stay` de quay demo.
- Kiem tra lai `Space`, `Right Arrow`, `Left Arrow`, bang diem va mau box tren ban GUI hien tai truoc khi ghi hinh.
- Lay so lieu UCS/A* va ket qua kiem chung heuristic tu cac lan chay that cua cac thanh vien phu trach Req 1-4; khong dien so lieu uoc tinh.
- Nhom bo sung ten, MSSV, email, phan tram dong gop va anh chup man hinh that truoc khi nop.
