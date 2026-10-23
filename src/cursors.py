"""Ghép 15 con trỏ: hình con trỏ + đầu Seele trên khung 32×32.

Mỗi con trỏ gồm danh sách khung (ảnh 32×32, thời lượng tính bằng jiffy
1/60 s) và điểm click. Con trỏ một khung xuất .cur, nhiều khung xuất .ani.
"""

from dataclasses import dataclass, field

from PIL import Image

import shapes
from head import head
from sprite import outlined, stamp

SIZE = 32
HEAD_POS = (10, 10)


@dataclass
class Cursor:
    number: int
    file: str  # tên file không đuôi
    title: str
    hotspot: tuple
    frames: list = field(default_factory=list)  # [(Image, jiffies)]

    @property
    def animated(self):
        return len(self.frames) > 1

    @property
    def filename(self):
        return f"{self.file}.{'ani' if self.animated else 'cur'}"


def canvas(expression=None):
    img = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    if expression:
        img.alpha_composite(head(expression), HEAD_POS)
    return img


def frame(expression, *layers):
    """layers: các bộ (lưới, x, y) vẽ đè lên theo thứ tự."""
    img = canvas(expression)
    for rows, x, y in layers:
        stamp(img, rows, x, y)
    return img


def centered(rows):
    """Toạ độ để tâm lưới trùng tâm khung (15, 15)."""
    return 15 - len(rows[0]) // 2, 15 - len(rows) // 2


def build():
    s = shapes
    arrow = (s.ARROW, 0, 0)
    cursors = []

    def add(number, file, title, hotspot, frames):
        cursors.append(Cursor(number, file, title, hotspot, frames))

    add(1, "Normal", "Normal Select", (0, 0), [(frame("smile", arrow), 0)])
    add(2, "Help", "Help Select", (0, 0),
        [(frame("curious", arrow, (s.QUESTION, 11, 0)), 0)])
    add(3, "Working", "Working in Background", (0, 0), [
        (frame("blink" if i == 3 else "smile", arrow, (s.hourglass(i, small=True), 12, 1)), 15)
        for i in range(4)
    ])

    zz = [[], [(s.Z_SMALL, 11, 5)], [(s.Z_SMALL, 11, 5), (s.Z_BIG, 16, 0)], [(s.Z_BIG, 16, 0)]]
    add(4, "Busy", "Busy", (5, 6), [
        (frame("sleepy", (s.hourglass(i), 1, 1), *zz[i]), 20) for i in range(4)
    ])
    add(5, "Text", "Text Select", (5, 8), [(frame("smile", (s.IBEAM, 2, 0)), 0)])
    add(6, "Link", "Link Select", (4, 0), [(frame("happy", (s.HAND, 0, 0)), 0)])
    add(7, "Unavailable", "Unavailable", (7, 7), [(frame("teary", (s.NO_SIGN, 0, 0)), 0)])
    add(8, "Handwriting", "Handwriting", (0, 0),
        [(frame("focused", (outlined(s.PEN), -1, -1)), 0)])
    add(9, "Person", "Person Select / Location Select", (5, 5),
        [(frame("blush", (s.HEART, 0, 0)), 0)])
    add(10, "Precision", "Precision Select", (8, 8),
        [(frame("determined", (s.CROSS, 0, 0)), 0)])
    for number, file, title, rows in [
        (11, "Move", "Move", s.SIZE_ALL),
        (12, "Horizontal", "Horizontal Resize", s.SIZE_WE),
        (13, "Vertical", "Vertical Resize", s.SIZE_NS),
        (14, "Diagonal1", "Diagonal Resize 1", s.SIZE_NWSE),
        (15, "Diagonal2", "Diagonal Resize 2", s.SIZE_NESW),
    ]:
        add(number, file, title, (15, 15), [(frame(None, (rows, *centered(rows))), 0)])
    return cursors


def scaled(img, size):
    if img.width == size:
        return img
    return img.resize((size, size), Image.NEAREST)


def scaled_hotspot(hotspot, size):
    return tuple(int(v * size / SIZE) for v in hotspot)
