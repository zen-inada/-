# mybot.py の例（最も左上から置ける場所に置くだけの超シンプル版）
def get_move(board):
    # board[z][y][x]（4x4x4）/ 空き(0), 先手(1), 後手(2)
    for y in range(4):
        for x in range(4):
            # 一番上(z=3)が空ならその列(x,y)に置ける
            if board[3][y][x] == 0:
                return (x, y)
    return (0, 0)  # フォールバック
