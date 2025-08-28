# === main.py（このファイルで MyAI.get_move の中身だけ自由に編集可）===

from abc import ABC, abstractmethod
from typing import Tuple, List
import random

Board = List[List[List[int]]]  # board[z][y][x]

# 変更禁止: 親クラス（契約）
class Alg3D(ABC):
    """
    3D四目アルゴリズムの親クラス
    学生はこのクラスを継承して get_move を実装する
    """
    @abstractmethod
    def get_move(self, board: Board) -> Tuple[int, int]:
        """
        次の手を返すメソッド
        board[z][y][x] 形式で石の配置が入る (0=空, 1=黒, 2=白)
        戻り値は (x, y) のタプル
        """
        ...

# ここから下だけロジックを編集
class MyAI(Alg3D):
    SIZE = 4
    # 3D 方向（反対向きは走査でカバーするので片側だけ列挙）
    DIRECTIONS = [
        (1, 0, 0), (0, 1, 0), (0, 0, 1),
        (1, 1, 0), (-1, 1, 0),
        (1, 0, 1), (0, 1, 1),
        (1, 1, 1), (-1, 1, 1), (1, -1, 1)
    ]

    def get_move(self, board: Board) -> Tuple[int, int]:
        # --- 手番推定（石の数から）---
        cnt1 = sum(board[z][y][x] == 1
                   for z in range(self.SIZE)
                   for y in range(self.SIZE)
                   for x in range(self.SIZE))
        cnt2 = sum(board[z][y][x] == 2
                   for z in range(self.SIZE)
                   for y in range(self.SIZE)
                   for x in range(self.SIZE))
        me = 1 if cnt1 <= cnt2 else 2
        opp = 3 - me

        legal = self._all_legal_moves(board)
        if not legal:
            return (0, 0)

        # ① 即勝ち手
        for x, y in legal:
            if self._wins_if_play(board, x, y, me):
                return (x, y)

        # ② 相手の即勝ちをブロック
        for x, y in legal:
            if self._wins_if_play(board, x, y, opp):
                return (x, y)

        # ③ 簡易スコアで選ぶ
        best_score = -10**9
        best_moves: List[Tuple[int, int]] = []
        for (x, y) in legal:
            s = self._score_move(board, x, y, me)
            if s > best_score:
                best_score = s
                best_moves = [(x, y)]
            elif s == best_score:
                best_moves.append((x, y))
        return random.choice(best_moves) if best_moves else (0, 0)

    # ====== 以降は補助メソッド ======
    def _in_bounds(self, x: int, y: int, z: int) -> bool:
        return 0 <= x < self.SIZE and 0 <= y < self.SIZE and 0 <= z < self.SIZE

    def _top_z(self, board: Board, x: int, y: int) -> int:
        for z in range(self.SIZE):
            if board[z][y][x] == 0:
                return z
        return -1  # 満杯

    def _check_win_from(self, board: Board, x: int, y: int, z: int, player: int) -> bool:
        for dx, dy, dz in self.DIRECTIONS:
            count = 1
            # 正方向
            for d in range(1, 4):
                nx, ny, nz = x + dx * d, y + dy * d, z + dz * d
                if self._in_bounds(nx, ny, nz) and board[nz][ny][nx] == player:
                    count += 1
                else:
                    break
            # 逆方向
            for d in range(1, 4):
                nx, ny, nz = x - dx * d, y - dy * d, z - dz * d
                if self._in_bounds(nx, ny, nz) and board[nz][ny][nx] == player:
                    count += 1
                else:
                    break
            if count >= 4:
                return True
        return False

    def _wins_if_play(self, board: Board, x: int, y: int, player: int) -> bool:
        z = self._top_z(board, x, y)
        if z == -1:
            return False
        board[z][y][x] = player
        try:
            return self._check_win_from(board, x, y, z, player)
        finally:
            board[z][y][x] = 0  # 差分だけ元に戻す

    def _score_move(self, board: Board, x: int, y: int, player: int) -> int:
        z = self._top_z(board, x, y)
        if z == -1:
            return -1  # 非合法
        score = 0
        for dx, dy, dz in self.DIRECTIONS:
            own = 0
            empties = 0
            # この手を通る方向で -3..+3 の範囲を見る
            for d in range(-3, 4):
                nx, ny, nz = x + dx * d, y + dy * d, z + dz * d
                if self._in_bounds(nx, ny, nz):
                    v = board[nz][ny][nx]
                    if v == player:
                        own += 1
                    elif v == 0:
                        empties += 1
            # 自石2以上かつ空き2以上のラインを少し優先
            if own >= 2 and empties >= 2:
                score += 1
        return score

    def _all_legal_moves(self, board: Board) -> List[Tuple[int, int]]:
        return [(x, y)
                for y in range(self.SIZE)
                for x in range(self.SIZE)
                if self._top_z(board, x, y) != -1]

# ---- 変更禁止：ワーカーが呼ぶエントリポイント ----
_ai = MyAI()

def get_move(board: Board) -> Tuple[int, int]:
    print("send_board")  # ログ（ワーカー側でstderrに回収されます）:contentReference[oaicite:1]{index=1}
    x, y = _ai.get_move(board)
    x, y = int(x), int(y)
    if not (0 <= x < 4 and 0 <= y < 4):
        raise ValueError(f"move out of range: {(x, y)}")
    return x, y

# main.py の末尾（変更可領域でOK）
def get_move(board):
    return MyAI().get_move(board)

