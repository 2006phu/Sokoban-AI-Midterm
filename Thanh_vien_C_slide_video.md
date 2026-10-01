# Thanh vien C - Slide va video demo

Storyboard cho phan trinh bay cua nhom. Dat ti le slide 4:3, nen sang, chu den va chi dung mau dam de danh dau agent/box.

## Noi dung 14 slide

1. **Trang bia** - Dai hoc Ton Duc Thang, mon Nhap mon Tri tue Nhan tao, de tai `Sokoban - Search Algorithms`, ten nhom.
2. **Thanh vien** - MSSV, ho ten, email, nhiem vu va phan tram hoan thanh cua tung nguoi.
3. **Mo hinh single-player** - State `(agent_pos, boxes)`, action North/South/East/West, goal test va cost.
4. **Mo hinh transition** - Agent di vao o trong; neu gap box thi day box neu o phia sau hop le.
5. **UCS** - Pseudocode muc y tuong: mo frontier theo chi phi nho nhat, mo rong state, cap nhat chi phi.
6. **A\*** - Pseudocode muc y tuong: uu tien `f(n) = g(n) + h(n)` va bo qua state da co chi phi tot hon.
7. **Heuristic** - BFS tinh khoang cach box-goal; Hungarian ghep box va goal voi tong chi phi nho nhat.
8. **Ket qua thi nghiem** - Dien bang UCS/A*: so state mo rong, so buoc, thoi gian; them bieu do neu co so lieu.
9. **Kiem chung heuristic** - Admissible khong danh gia qua; consistent thoa `h(s) <= cost(s,s') + h(s')`; chen ket qua file kiem chung cua nhom.
10. **GUI single-player** - Anh chup man hinh va ba phim Space, Right Arrow, Left Arrow.
11. **Competitive: mo hinh** - Hai agent chon dong thoi trong 5 action, toi da `n` buoc, va diem la so box cua minh tren goal.
12. **Competitive: GUI va chien luoc** - Agent 1 xanh, agent 2 do cam; box neutral nau; box da ghi diem co mau theo chu so huu; xu ly cung o va swap.
13. **Bang hoan thanh** - Req 1 den Req 8, noi dung va phan tram dong gop theo trang thai da kiem chung.
14. **Uu nhuoc diem** - Uu: A* nhanh, heuristic co co so, GUI de theo doi. Nhuoc: chua xu ly deadlock phuc tap va chat luong agent phu thuoc chien luoc.

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