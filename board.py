import random
from collections import deque

ROWS = 10
COLS = 10
NUM_MINES = 10

board = [[0 for _ in range(COLS)] for _ in range(ROWS)]
revealed = [[False for _ in range(COLS)] for _ in range(ROWS)]
flagged = [[False for _ in range(COLS)] for _ in range(ROWS)]

mines = set()
while len(mines) < NUM_MINES:
    r = random.randint(0, ROWS - 1)
    c = random.randint(0, COLS - 1)
    mines.add((r, c))

for r, c in mines:
    board[r][c] = -1

for r, c in mines:
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < ROWS and 0 <= nc < COLS and board[nr][nc] != -1:
                board[nr][nc] += 1

last_move = (-1, -1)

def color_text(text, color_code):
    return f"\033[{color_code}m{text}\033[0m"

def print_board():
    print("\nPapan:")
    for i in range(ROWS):
        row_str = ''
        for j in range(COLS):
            cell_str = ''
            if revealed[i][j]:
                if board[i][j] == -1:
                    cell_str = color_text('*', '1;31')  # merah tebal
                elif board[i][j] == 0:
                    cell_str = '.'
                else:
                    color_map = {'1': '1;34', '2': '1;32', '3': '1;31', '4': '1;35', '5': '1;36', '6': '1;33', '7': '1;34', '8': '1;32'}
                    color_code = color_map.get(str(board[i][j]), '1;37')
                    cell_str = color_text(str(board[i][j]), color_code)
            elif flagged[i][j]:
                cell_str = color_text('⚑', '1;33')  # kuning tebal, simbol flag
            else:
                cell_str = color_text('X', '1;37')  # putih tebal

            if (i, j) == last_move:
                row_str += f'[{cell_str}] '
            else:
                row_str += f' {cell_str}  '
        print(row_str)

def reveal_area(r, c):
    queue = deque()
    queue.append((r, c))
    visited = set()

    while queue:
        cr, cc = queue.popleft()
        if (cr, cc) in visited or revealed[cr][cc]:
            continue
        visited.add((cr, cc))
        revealed[cr][cc] = True

        if board[cr][cc] == 0:
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    nr, nc = cr + dr, cc + dc
                    if 0 <= nr < ROWS and 0 <= nc < COLS:
                        queue.append((nr, nc))

def reveal_all_mines():
    for r, c in mines:
        revealed[r][c] = True

def check_win():
    all_clear = True
    all_flags_correct = True
    for i in range(ROWS):
        for j in range(COLS):
            if board[i][j] != -1 and not revealed[i][j]:
                all_clear = False
            if flagged[i][j] != ((i, j) in mines):
                all_flags_correct = False
    return all_clear or all_flags_correct

while True:
    print_board()
    if check_win():
        print("\n\033[1;32mSelamat! Anda menang!\033[0m")
        break

    try:
        inp = input("Masukkan koordinat + opsi (baris kolom o/f), misal 3 4 o (open) atau 3 4 f (flag): ")
        parts = inp.strip().split()
        if len(parts) != 3:
            print("Format input salah!")
            continue
        r, c, action = int(parts[0]) - 1, int(parts[1]) - 1, parts[2].lower()
        if 0 <= r < ROWS and 0 <= c < COLS:
            last_move = (r, c)
            if revealed[r][c]:
                print("Kotak ini sudah terbuka!")
                continue
            if action == 'f':
                flagged[r][c] = not flagged[r][c]
            elif action == 'o':
                if flagged[r][c]:
                    print("Kotak ini sedang di-flag, unflag dulu untuk buka.")
                    continue
                if board[r][c] == -1:
                    reveal_all_mines()
                    print_board()
                    print("\033[1;31mBOOM! Kena bom. Game over!\033[0m")
                    break
                elif board[r][c] == 0:
                    reveal_area(r, c)
                else:
                    revealed[r][c] = True
            else:
                print("Aksi tidak dikenali! Gunakan 'o' (open) atau 'f' (flag).")
        else:
            print("Koordinat di luar papan!")
    except Exception as e:
        print(f"Input tidak valid: {e}")
