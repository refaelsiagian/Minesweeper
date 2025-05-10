import random

# Ukuran papan
ROWS = 10
COLS = 10
NUM_MINES = 10

# Inisialisasi papan kosong
board = [[0 for _ in range(COLS)] for _ in range(ROWS)]

# Sebar bom secara acak
mines = set()
while len(mines) < NUM_MINES:
    r = random.randint(0, ROWS - 1)
    c = random.randint(0, COLS - 1)
    mines.add((r, c))

# Tandai bom di papan
for r, c in mines:
    board[r][c] = -1  # Gunakan -1 untuk mewakili bom

# Hitung angka di sekitar bom
for r, c in mines:
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < ROWS and 0 <= nc < COLS and board[nr][nc] != -1:
                board[nr][nc] += 1

# Tampilkan papan (hanya untuk debug)
for row in board:
    row_str = ' '.join(['*' if cell == -1 else str(cell) for cell in row])
    print(row_str)
