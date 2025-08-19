def get_move(board):
    print("send_board")  # ハンドシェイク

    import random

    SIZE = 4

    directions = [
        (1, 0, 0), (0, 1, 0), (0, 0, 1),
        (1, 1, 0), (-1, 1, 0), (1, 0, 1), (0, 1, 1),
        (1, 1, 1), (-1, 1, 1), (1, -1, 1)
    ]

    def is_valid(x, y, z):
        return 0 <= x < SIZE and 0 <= y < SIZE and 0 <= z < SIZE

    def get_top_z(x, y):
        for z in range(SIZE):
            if board[z][y][x] == 0:
                return z
        return -1

    def check_win(x, y, z, player):
        for dx, dy, dz in directions:
            count = 1
            for d in range(1, 4):
                nx, ny, nz = x + dx * d, y + dy * d, z + dz * d
                if is_valid(nx, ny, nz) and board[nz][ny][nx] == player:
                    count += 1
                else:
                    break
            for d in range(1, 4):
                nx, ny, nz = x - dx * d, y - dy * d, z - dz * d
                if is_valid(nx, ny, nz) and board[nz][ny][nx] == player:
                    count += 1
                else:
                    break
            if count >= 4:
                return True
        return False

    def simulate(x, y, player):
        z = get_top_z(x, y)
        if z == -1:
            return False
        board[z][y][x] = player
        win = check_win(x, y, z, player)
        board[z][y][x] = 0
        return win

    def score_move(x, y, player):
        z = get_top_z(x, y)
        if z == -1:
            return -1  # illegal
        score = 0
        for dx, dy, dz in directions:
            line = []
            for d in range(-3, 4):
                nx, ny, nz = x + dx * d, y + dy * d, z + dz * d
                if is_valid(nx, ny, nz):
                    line.append(board[nz][ny][nx])
            if line.count(player) >= 2 and line.count(0) >= 2:
                score += 1
        return score

    def get_all_moves():
        return [(x, y) for x in range(SIZE) for y in range(SIZE) if get_top_z(x, y) != -1]

    # 判定用：自分と相手のターンを数から推定
    count1 = sum(board[z][y][x] == 1 for z in range(SIZE) for y in range(SIZE) for x in range(SIZE))
    count2 = sum(board[z][y][x] == 2 for z in range(SIZE) for y in range(SIZE) for x in range(SIZE))
    me = 1 if count1 <= count2 else 2
    opp = 3 - me

    legal = get_all_moves()

    # ① 勝ち手
    for x, y in legal:
        if simulate(x, y, me):
            return (x, y)

    # ② ブロック
    for x, y in legal:
        if simulate(x, y, opp):
            return (x, y)

    # ③ スコア評価
    scored = [(score_move(x, y, me), (x, y)) for x, y in legal]
    max_score = max(s[0] for s in scored)
    best = [move for score, move in scored if score == max_score]

    return random.choice(best) if best else (0, 0)
