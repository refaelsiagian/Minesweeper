import random

# Ukuran papan
ROWS = 10
COLS = 10
NUM_MINES = 10

# Inisialisasi papan kosong
board = [[0 for _ in range(COLS)] for _ in range(ROWS)]
# Papan penutup (False = tertutup, True = terbuka)
revealed = [[False for _ in range(COLS)] for _ in range(ROWS)]

# Sebar bom secara acak
mines = set()
while len(mines) < NUM_MINES:
    r = random.randint(0, ROWS - 1)
    c = random.randint(0, COLS - 1)
    mines.add((r, c))

# Tandai bom di papan
for r, c in mines:
    board[r][c] = -1  # Gunakan -1 untuk bom

# Hitung angka di sekitar bom
for r, c in mines:
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < ROWS and 0 <= nc < COLS and board[nr][nc] != -1:
                board[nr][nc] += 1

def print_board():
    print("\nPapan:")
    for i in range(ROWS):
        row_str = ''
        for j in range(COLS):
            if revealed[i][j]:
                if board[i][j] == -1:
                    row_str += '* '
                else:
                    row_str += f'{board[i][j]} '
            else:
                row_str += 'X '
        print(row_str)

# Main loop
while True:
    print_board()
    try:
        inp = input("Masukkan koordinat (baris kolom, mulai dari 1), misal 3 4: ")
        r, c = map(int, inp.strip().split())
        r -= 1  # Sesuaikan ke indeks 0
        c -= 1
        if 0 <= r < ROWS and 0 <= c < COLS:
            revealed[r][c] = True
            if board[r][c] == -1:
                print_board()
                print("BOOM! Kena bom. Game over!")
                break
        else:
            print("Koordinat di luar papan!")
    except Exception as e:
        print(f"Input tidak valid: {e}")
