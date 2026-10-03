# KẾ HOẠCH & KỊCH BẢN QUAY VIDEO DEMO ĐỒ ÁN SOKOBAN AI

> **Môn học:** Nhập môn Trí tuệ Nhân tạo (503043) — Đại học Tôn Đức Thắng  
> **Quy định thời lượng (Mục III - GK.md):** Tối đa **03 phút (180 giây)**.  
> **Thời lượng mục tiêu kịch bản:** **02 phút 40 giây — 02 phút 45 giây** *(Đảm bảo an toàn tuyệt đối dưới 3:00)*  
> **Sản phẩm bàn giao:** File `demo.txt` chứa liên kết video (YouTube Unlisted hoặc Google Drive mở quyền xem công khai).

---

## 1. THÔNG SỐ KỸ THUẬT & CHUẨN BỊ QUAY

### 1.1. Cấu hình phần mềm quay màn hình
- **Phần mềm khuyến nghị:** **OBS Studio** (miễn phí, chất lượng cao nhất) hoặc **Xbox Game Bar** (`Win + G` trên Windows).
- **Độ phân giải:** `1920 x 1080` (Full HD), tỉ lệ khung hình `16:9`.
- **Tốc độ khung hình (FPS):** `30 FPS` hoặc `60 FPS` để hoạt cảnh di chuyển mượt mà.
- **Terminal setup:** Visual Studio Code hoặc Windows Terminal, phóng to font chữ lên **16pt - 18pt** (rõ nét khi xem trên điện thoại/máy chiếu).
- **Âm thanh / Microphone:**
  - Bật bộ lọc loại bỏ tiếng ồn (*Noise Suppression*) trong OBS.
  - **Khuyến nghị cách làm tốt nhất:** **Quay video thao tác màn hình trước (không cần nói) -> Dùng CapCut hoặc Microsoft Clipchamp lồng tiếng (Voice-over) sau**. Cách này giúp lời nói khớp 100% với hành động, không lo bị vấp, không có tạp âm và kiểm soát thời lượng chính xác đến từng giây.

---

## 2. BẢNG PHÂN BỔ THỜI LƯỢNG (TIMELINE TỔNG QUAN)

| Phân đoạn | Nội dung chính | Thời lượng | Mốc thời gian |
| :---: | :--- | :---: | :---: |
| **Phần 0** | Mở đầu: Giới thiệu đề tài & các thành viên | **15s** | `0:00 - 0:15` |
| **Phần 1** | Task 1: Demo Single Agent UCS trên GUI Pygame | **30s** | `0:15 - 0:45` |
| **Phần 2** | Task 1: Demo A* với Heuristic Hungarian + BFS | **30s** | `0:45 - 1:15` |
| **Phần 3** | Task 1: Chạy thực nghiệm & kiểm chứng Heuristic | **20s** | `1:15 - 1:35` |
| **Phần 4** | Task 1 Competitive: Khởi chạy chế độ 2-Agent & nhập $n$ bước | **20s** | `1:35 - 1:55` |
| **Phần 5** | Task 1 Competitive: Trận đấu 2 Agent, cướp hộp, phân định thắng thua | **35s** | `1:55 - 2:30` |
| **Phần 6** | Tổng kết: Lời kết & thông tin nộp bài | **15s** | `2:30 - 2:45` |
| **Dự phòng**| Khoảng đệm an toàn trước mốc 3:00 | **15s** | `2:45 - 3:00` |

---

## 3. KỊCH BẢN CHI TIẾT TỪNG PHÂN CẢNH (SCENE-BY-SCENE SCRIPT)

### CẢNH 1: MỞ ĐẦU & GIỚI THIỆU (0:00 – 0:15)
- **Hình ảnh trên màn hình:**
  - Mở VS Code hiển thị cấu trúc project hoặc mở slide tiêu đề bìa báo cáo.
  - Hiện rõ: Tên đồ án *Sokoban AI*, Môn học *503043*, Nhóm thực hiện.
- **Thao tác:** Con trỏ chuột chỉ nhẹ vào 2 thư mục `source/task1` và `source/task1_competitive`.
- **Lời thoại (Voice-over):**
  > *"Kính chào thầy cô và các bạn! Đây là video demo đồ án Giữa kỳ môn Nhập môn Trí tuệ Nhân tạo của nhóm chúng em với đề tài Game Sokoban. Dự án gồm hai nội dung chính: Task 1 - Giải quyết bài toán Sokoban đơn tác tử bằng các thuật toán tìm kiếm không gian trạng thái, và Task 1 Competitive - Chế độ thi đấu đối kháng thời gian thực giữa hai Agent với cơ chế cướp hộp độc đáo."*

---

### CẢNH 2: TASK 1 — DEMO THUẬT TOÁN UCS (0:15 – 0:45)
- **Hình ảnh trên màn hình:**
  - Mở terminal tại thư mục `source/task1`:
    ```powershell
    cd source/task1
    python main.py
    ```
  - Chọn bản đồ `ez_map.txt` (hoặc nhấn phím tương ứng) -> Chọn thuật toán `1` (Uniform Cost Search).
  - Cửa sổ Pygame hiện lên giao diện game Sokoban trực quan:
    - Bàn cờ đồ họa rõ ràng.
    - Panel thông số: Số bước (`Cost`), Số node mở rộng (`Nodes Expanded`), Kích thước frontier, Thời gian thực thi.
- **Thao tác:**
  - Nhấn phím `Space`: Agent tự động di chuyển vài bước.
  - Nhấn `Space` một lần nữa để **Tạm dừng (Pause)**.
  - Nhấn phím `Left Arrow` (`<-`): Tua lùi lại 2 bước.
  - Nhấn phím `Right Arrow` (`->`): Bước tới 2 bước.
  - Nhấn `Space` để tiếp tục chạy tự động cho đến khi hoàn thành màn chơi (Trạng thái chuyển sang `COMPLETED`).
- **Lời thoại (Voice-over):**
  > *"Bắt đầu với Task 1, chúng em tiến hành giải bài toán bằng thuật toán Uniform Cost Search. Giao diện Pygame được thiết kế hoàn chỉnh, hỗ trợ tương tác thân thiện: người dùng có thể nhấn Space để tạm dừng hoặc tiếp tục chạy tự động, dùng các phím mũi tên Trái - Phải để lùi hoặc tiến từng bước một cách linh hoạt. Panel thông tin hiển thị chính xác chi phí đường đi, số node đã mở rộng và thời gian tìm kiếm."*

---

### CẢNH 3: TASK 1 — DEMO THUẬT TOÁN A* VỚI HEURISTIC (0:45 – 1:15)
- **Hình ảnh trên màn hình:**
  - Đóng cửa sổ cũ, chạy lại `python main.py` -> Chọn `2` (A* Search) trên cùng bản đồ.
  - Cửa sổ Pygame mở ra, cho agent chạy về đích.
  - So sánh trực quan thông số số node mở rộng giữa A* và UCS.
- **Thao tác:**
  - Nhấn `Space` cho chạy tự động đến khi giải xong.
  - Di chuột vào dòng thông số trên Terminal / Panel để người xem thấy sự khác biệt về số node.
- **Lời thoại (Voice-over):**
  > *"Tiếp theo là thuật toán A*. Nhóm đã đề xuất hàm Heuristic kết hợp giữa BFS tính khoảng cách thực tế trên lưới không chướng ngại vật với thuật toán Hungarian để ghép cặp tối ưu giữa các hộp và các vị trí đích. Nhờ định hướng thông minh của hàm đánh giá f(n) = g(n) + h(n), số lượng node mà A* cần mở rộng giảm đáng kể so với UCS, giúp thuật toán tìm ra lời giải tối ưu chỉ trong chớp mắt."*

---

### CẢNH 4: TASK 1 — KIỂM CHỨNG HEURISTIC & EXPERIMENT (1:15 – 1:35)
- **Hình ảnh trên màn hình:**
  - Trên terminal, chạy lệnh kiểm chứng tính chất:
    ```powershell
    python heuristic_verification.py
    ```
  - Bảng kết quả hiển thị 100% trạng thái kiểm tra đều thỏa mãn:
    - `h(n) <= h*(n)` (Tính Admissible).
    - `h(n) <= c(n, a, n') + h(n')` (Tính Consistent / Monotonic).
  - Tiếp tục chạy lệnh thực nghiệm so sánh:
    ```powershell
    python experiment.py
    ```
  - Bảng số liệu Benchmark so sánh Time & Space giữa Easy, Medium, Hard hiện ra đầy đủ.
- **Thao tác:** Cuộn nhẹ màn hình terminal hiển thị dòng tổng kết kết quả.
- **Lời thoại (Voice-over):**
  > *"Để đảm bảo tính đúng đắn khoa học, nhóm đã xây dựng script kiểm chứng tự động chứng minh 100% trạng thái đều thỏa mãn tính Admissible và Consistent. Đồng thời, script Benchmark đo lường độc lập đã thể hiện rõ độ phức tạp không gian và thời gian vượt trội của A* trên nhiều cấp độ bản đồ khác nhau."*

---

### CẢNH 5: TASK 1 COMPETITIVE — KHỞI ĐỘNG CHẾ ĐỘ THI ĐẤU 2-AGENT (1:35 – 1:55)
- **Hình ảnh trên màn hình:**
  - Chuyển terminal sang thư mục thi đấu:
    ```powershell
    cd ../task1_competitive
    python main.py
    ```
  - Terminal in ra thông tin bản đồ thi đấu, vị trí ban đầu của Agent 1 và Agent 2.
  - Dòng yêu cầu nhập: `Nhap so buoc thi dau n (Mac dinh: 60):` -> Nhập `60` và Enter.
  - Cửa sổ Pygame mở ra giao diện thi đấu:
    - Agent 1: Màu xanh dương.
    - Agent 2: Màu đỏ cam.
    - Các hộp trung lập: Màu nâu cam (`P` trống).
    - Bảng tỉ số góc trên cùng: Điểm số của từng agent và số bước còn lại.
- **Thao tác:** Di chuyển cửa sổ Pygame vào chính giữa màn hình, sẵn sàng bấm `Space`.
- **Lời thoại (Voice-over):**
  > *"Chuyển sang chế độ thi đấu đối kháng hai Agent. Bài toán được thiết kế trên một bản đồ đối xứng mở rộng. Người dùng có thể thiết lập số bước thi đấu n tùy ý, ở đây chúng em đặt n = 60 bước. Hai agent được điều khiển bởi hai file mã nguồn độc lập, cho phép sẵn sàng thi đấu trực tiếp giữa các nhóm học viên."*

---

### CẢNH 6: TASK 1 COMPETITIVE — ĐẤU TRÍ, CƯỚP HỘP & PHÂN XỬ (1:55 – 2:30)
- **Hình ảnh trên màn hình:**
  - Nhấn `Space` để 2 agent bắt đầu trận đấu tự động.
  - Quan sát trực quan các tình huống nổi bật:
    1. **Chiếm hộp:** Khi Agent 1 đẩy hộp vào goal -> Hộp lập tức đổi sang **màu xanh dương kèm nhãn P1**. Khi Agent 2 đẩy vào goal -> Hộp đổi sang **màu cam đỏ kèm nhãn P2**. Điểm số trên panel cập nhật tương ứng theo thời gian thực.
    2. **Cướp hộp đối thủ:** Agent chủ động di chuyển tới đẩy hộp của đối phương ra khỏi vị trí goal để làm đối thủ bị trừ điểm và đoạt lấy cơ hội.
    3. **Giải quyết xung đột:** Khi 2 agent cùng di chuyển vào một ô hoặc đối đầu nhau, cơ chế phân xử xung đột tự động giữ an toàn, hai agent không bị đi xuyên qua nhau.
  - Hết 60 bước: Trận đấu kết thúc, hệ thống hiển thị nổi bật banner chiến thắng: `WINNER: AGENT 1!` (hoặc kết quả trận đấu).
- **Thao tác:** Để trận đấu chạy mượt mà. Khi có pha cướp hộp hoặc đổi màu hộp, có thể tạm dừng 1-2 giây để người xem chú ý rồi nhấn `Space` tiếp tục.
- **Lời thoại (Voice-over):**
  > *"Mỗi lượt chơi, cả hai agent chọn hành động đồng thời với thời gian tính toán cực nhanh dưới 10 miligiây. Điểm sáng tạo của nhóm là cơ chế sở hữu hộp linh hoạt: hộp được agent nào đưa vào đích sẽ đổi màu đại diện cho agent đó. Đồng thời, các agent được tích hợp chiến thuật cướp hộp đối kháng — sẵn sàng đẩy bật hộp đối thủ ra ngoài để lật ngược tình thế. Khi kết thúc 60 bước, hệ thống sẽ tự động tổng kết và vinh danh tác tử chiến thắng."*

---

### CẢNH 7: TỔNG KẾT & KẾT THÚC (2:30 – 2:45)
- **Hình ảnh trên màn hình:**
  - Chuyển về màn hình GitHub repository hoặc slide kết thúc có dòng chữ:  
    *Cảm ơn Thầy Cô đã theo dõi video demo!*
  - Mở nhanh file `demo.txt` minh họa.
- **Lời thoại (Voice-over):**
  > *"Toàn bộ mã nguồn đã được đóng gói chuẩn mực theo mô hình hướng đối tượng, kiểm thử tương thích hoàn hảo trên cả macOS và Windows. Cảm ơn thầy cô và các bạn đã dành thời gian theo dõi phần trình diễn của nhóm chúng em!"*

---

## 4. CHECKLIST THỰC HÀNH KHI QUAY VIDEO

### Các câu lệnh chuẩn bị sẵn trong Terminal:
```powershell
# Cửa sổ 1: Dành cho Task 1 (Single Agent)
cd d:\University\AI\GK\source\task1
python main.py
python heuristic_verification.py
python experiment.py

# Cửa sổ 2: Dành cho Task 1 Competitive
cd d:\University\AI\GK\source\task1_competitive
python main.py
```

### Các phím tắt điều khiển Pygame cần nhớ:
- **`SPACE`**: Bắt đầu / Tạm dừng (Play / Pause).
- **`RIGHT ARROW` (`->`)**: Bước tới 1 bước (Next step).
- **`LEFT ARROW` (`<-`)**: Lùi lại 1 bước (Previous step).
- **`R`**: Reset lại trạng thái ban đầu của bàn cờ.
- **`ESC`**: Thoát cửa sổ game.

---

## 5. HƯỚNG DẪN TẠO FILE `demo.txt` ĐỂ NỘP BÀI

Theo yêu cầu nộp bài tại **Mục III (`GK.md`)**:
1. Đăng tải video lên **YouTube** (đặt chế độ **Không công khai / Unlisted**) hoặc tải lên **Google Drive** (chọn quyền chia sẻ: **"Bất kỳ ai có đường liên kết đều có thể xem"**).
2. Tạo file `demo.txt` đặt tại thư mục nộp bài với nội dung mẫu chuẩn:

```text
DO AN GIUA KY - MON NHAP MON TRI TUE NHAN TAO (503043)
De tai: Game Sokoban (Single Agent & Competitive 2-Agent)
Nhom: [Dien ma nhom cua ban]

LIEN KET VIDEO DEMO:
https://youtu.be/xxxxxxxxx (hoac link Google Drive cua nhom)

Thoi luong video: 02 phut 42 giay (Tuan thu quy dinh toi da 03 phut)
Moi truong thu nghiem: Python 3.14 / pygame-ce / Windows & macOS Ventura
```

> **LƯU Ý QUAN TRỌNG:** Hãy mở đường link trong file `demo.txt` bằng **Tab ẩn danh (Incognito Window)** trên trình duyệt để chắc chắn rằng bất kỳ ai (kể cả giảng viên chấm bài không đăng nhập) đều có thể xem được video ngay lập tức!
