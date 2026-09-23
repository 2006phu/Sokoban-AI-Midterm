# Sokoban AI — Midterm Project
# Môn: Nhập môn Trí tuệ Nhân tạo (503043)
# Trường: Đại học Tôn Đức Thắng

## Yêu cầu hệ thống
- Python 3.x
- pygame
- scipy (cho Hungarian Algorithm)

## Cài đặt
```bash
pip install -r source/task1/requirements.txt
```

## Chạy chương trình

### Task 1: Sokoban Single-player
```bash
cd source/task1
python main.py
```

### Task 1 Competitive: Sokoban 2-Agent
```bash
cd source/task1_competitive
python main.py
```

## Cấu trúc thư mục
```
source/
├── task1/                    # Single-player Sokoban
│   ├── main.py               # Entry point
│   ├── game_map.py           # Đọc và quản lý bản đồ
│   ├── state.py              # Trạng thái game
│   ├── solver.py             # UCS + A*
│   ├── heuristic.py          # Hàm heuristic
│   ├── gui.py                # Giao diện pygame
│   ├── experiment.py         # Thí nghiệm so sánh
│   ├── heuristic_verification.py
│   └── maps/
│       └── example_map.txt
│
└── task1_competitive/        # 2-Agent Competitive
    ├── main.py
    ├── game_map.py
    ├── state.py
    ├── agent_algorithm.py    # Thuật toán agent (file riêng)
    ├── competitive_gui.py
    └── maps/
        └── competitive_map.txt
```

## Điều khiển
- **Space**: Pause/Resume
- **→ (Right Arrow)**: Di chuyển tiến 1 bước
- **← (Left Arrow)**: Di chuyển lùi 1 bước
- Chọn thuật toán: UCS hoặc A*
