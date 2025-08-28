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
    # 3D 方向（両向きを数えるので片側だけ列挙）
    DIRECTIONS = [
        (1, 0, 0), (0, 1, 0), (0, 0, 1),
        (1, 1, 0), (-1, 1, 0), (1, 0, 1), (0, 1, 1),
        (1, 1, 1), (-1, 1, 1), (1, -1, 1)
    ]

    def get_move(self, board: Board) -> Tuple[int, int]:
        # --- 手番推定（石の数から）---
        cnt1 = sum(board[z][y][x] == 1 for z in range(self.SIZE) for y in range(self.SIZE) for x in range(self.SIZE))
        cnt2 = sum(board[z][y][x] == 2 for z in range(self.SIZE) for y in range(self.SIZE) for x in range(self.SIZE))
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
        scored = [(self._score_move(board, x, y, me), (x, y)) for (x, y) in legal]
        best_score = max(s for s, _ in scored)
        candidates = [mv for s, mv in scored if s == best_score]
        return random.choice(candidates) if candidates else (0, 0)

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
        won = self._check_win_from(board, x, y, z, player)
        board[z][y][x] = 0  # 差分だけ元に戻す
        return won

    def _score_move(self, board: Board, x: int, y: int, player: int) -> int:
        z = self._top_z(board, x, y)
        if z == -1:
            return -1  # 非合法
        score = 0
        for dx, dy, dz in self.DIRECTIONS:
            line: List[int] = []
            for d in range(-3, 4):
                nx, ny,
