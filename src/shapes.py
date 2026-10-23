"""Hình con trỏ (mũi tên, I-beam, bàn tay…) dạng lưới ký tự.

Hình vẽ tay có sẵn viền 'O'; hình dựng bằng code được thêm viền qua `outlined`.
"""

from sprite import from_mask, mirror, outlined, overlay, parse, rotate90

ARROW = parse([
    "O..........",
    "OO.........",
    "OXO........",
    "OXXO.......",
    "OXXXO......",
    "OXXXXO.....",
    "OXXXXXO....",
    "OXXXXXXO...",
    "OXXXXXXXO..",
    "OXXXXXXXXO.",
    "OXXXXXXXXXO",
    "OXXXXXOOOOO",
    "OXXOXXO....",
    "OXO.OXXO...",
    "OO..OXXO...",
    "O....OXXO..",
    ".....OXXO..",
    "......OO...",
])

QUESTION = outlined([
    ".ccc.",
    "c...c",
    "....c",
    "...c.",
    "..c..",
    "..c..",
    ".....",
    "..c..",
])

IBEAM = parse([
    "OOO.OOO",
    "OXXOXXO",
    "OOOXOOO",
    "..OXO..",
    "..OXO..",
    "..OXO..",
    "..OXO..",
    "..OXO..",
    "..OXO..",
    "..OXO..",
    "..OXO..",
    "..OXO..",
    "..OXO..",
    "OOOXOOO",
    "OXXOXXO",
    "OOO.OOO",
])

HAND = parse([
    "....OO.........",
    "...OXXO........",
    "...OXXO........",
    "...OXXO........",
    "...OXXOOO......",
    "...OXXOXXOOO...",
    "...OXXOXXOXXOO.",
    ".OOOXXOXXOXXOXO",
    "OXXOXXXXXXXXOXO",
    "OXXXXXXXXXXXXXO",
    ".OXXXXXXXXXXXXO",
    "..OXXXXXXXXXXXO",
    "..OXXXXXXXXXXO.",
    "...OXXXXXXXXXO.",
    "....OXXXXXXXO..",
    "....OXXXXXXXO..",
    "....OOOOOOOOO..",
])


def _no_sign():
    c = 6.0

    def px(x, y):
        d = ((x - c) ** 2 + (y - c) ** 2) ** 0.5
        if d > 6.4:
            return "."
        if d >= 4.3 or abs(x - y) <= 1:
            return "r"
        return "X"

    return outlined(from_mask(13, 13, px))


NO_SIGN = _no_sign()


def _pen():
    def px(x, y):
        if abs(x - y) > 1 or x + y > 22:
            return "."
        s = x + y
        if s <= 2:
            return "k"  # ngòi
        if s >= 19:
            return "C"  # nắp xanh
        return "x" if x - y == 1 else "X"

    return from_mask(12, 12, px)


PEN = _pen()  # chưa có viền: viền thêm khi ghép, để ngòi chạm đúng (0,0)

HEART = outlined([
    ".ii...ii.",
    "iiii.iiii",
    "iXiiiiiii",
    "iiiiiiiiI",
    ".iiiiiiI.",
    "..iiiiI..",
    "...iiI...",
    "....I....",
])


def _cross():
    def px(x, y):
        if (x, y) == (7, 7):
            return "C"
        if (y == 7 and abs(x - 7) >= 3) or (x == 7 and abs(y - 7) >= 3):
            return "X"
        return "."

    return outlined(from_mask(15, 15, px))


CROSS = _cross()


def hourglass(frame, small=False):
    """Đồng hồ cát; frame 0-3 là cát chảy từ trên xuống dưới."""
    if small:
        rows = [
            "OOOOOOO",
            ".O111O.",
            ".O222O.",
            "..O3O..",
            "..OsO..",
            "..O3O..",
            ".O222O.",
            ".O111O.",
            "OOOOOOO",
        ]
    else:
        rows = [
            "OOOOOOOOO",
            "OYYYYYYYO",
            ".O11111O.",
            ".O22222O.",
            "..O333O..",
            "...OsO...",
            "..O333O..",
            ".O22222O.",
            ".O11111O.",
            "OYYYYYYYO",
            "OOOOOOOOO",
        ]
    half = len(rows) // 2
    out = []
    for y, row in enumerate(rows):
        line = ""
        for ch in row:
            if ch in "123":
                level = int(ch)
                if y < half:  # bầu trên: cạn dần từ trên xuống
                    line += "y" if level > frame else "x"
                else:  # bầu dưới: đầy dần từ đáy lên
                    line += "y" if level <= frame else "x"
            elif ch == "s":
                line += "y" if frame < 3 else "x"
            else:
                line += ch
        out.append(line)
    return out


def _z(big):
    if big:
        rows = ["XXXXX", "...X.", "..X..", ".X...", "XXXXX"]
    else:
        rows = ["XXXX", "..X.", ".X..", "XXXX"]
    return outlined(rows)


Z_BIG = _z(True)
Z_SMALL = _z(False)


def _size_we():
    # mũi tên hai đầu nằm ngang, thân 1 px
    length, height = 19, 7
    mid = height // 2

    def px(x, y):
        dy = abs(y - mid)
        if x < 4 and dy <= x:
            return "X"
        if x > length - 5 and dy <= length - 1 - x:
            return "X"
        if dy == 0:
            return "X"
        return "."

    return outlined(from_mask(length, height, px))


SIZE_WE = _size_we()
SIZE_NS = rotate90(SIZE_WE)


def _size_nwse():
    n = 15

    def px(x, y):
        if x + y <= 4 or (n - 1 - x) + (n - 1 - y) <= 4 or x == y:
            return "X"
        return "."

    return outlined(from_mask(n, n, px))


SIZE_NWSE = _size_nwse()
SIZE_NESW = mirror(SIZE_NWSE)


def _size_all():
    we = SIZE_WE
    pad = (len(we[0]) - len(we)) // 2
    blank = "." * len(we[0])
    we_sq = [blank] * pad + we + [blank] * pad
    ns_sq = rotate90(we_sq)
    combined = overlay(we_sq, ns_sq)
    # nối lại các ô viền bị đè lên phần thân của mũi tên kia
    size = len(combined)
    c = size // 2
    crystal = [
        "...c...",
        "..cCc..",
        ".cCWCc.",
        "cCWWWCc",
        ".cCWCc.",
        "..cCc..",
        "...c...",
    ]
    crystal = outlined(crystal)
    k = len(crystal) // 2
    grid = [list(r) for r in combined]
    # ô 'X' của trục bị viền 'O' của trục kia đè: khôi phục
    for y in range(size):
        for x in range(size):
            if (y == c and 1 <= x < size - 1) or (x == c and 1 <= y < size - 1):
                if grid[y][x] == "O":
                    grid[y][x] = "X"
    for y, row in enumerate(crystal):
        for x, ch in enumerate(row):
            if ch != ".":
                grid[c - k + y][c - k + x] = ch
    return ["".join(r) for r in grid]


SIZE_ALL = _size_all()

