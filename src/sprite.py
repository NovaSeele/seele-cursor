"""Tiện ích sprite: chuỗi ký tự -> ảnh RGBA, ghép lớp, lật."""

from PIL import Image

from palette import rgba


def parse(rows):
    """Kiểm tra lưới ký tự (mọi hàng cùng độ dài) và trả về danh sách hàng."""
    rows = [r for r in rows]
    width = len(rows[0])
    for i, r in enumerate(rows):
        if len(r) != width:
            raise ValueError(f"hàng {i} dài {len(r)}, cần {width}: {r!r}")
    return rows


def to_image(rows):
    rows = parse(rows)
    img = Image.new("RGBA", (len(rows[0]), len(rows)), (0, 0, 0, 0))
    px = img.load()
    for y, row in enumerate(rows):
        for x, ch in enumerate(row):
            px[x, y] = rgba(ch)
    return img


def stamp(base, rows, x0, y0):
    """Vẽ đè lưới ký tự lên ảnh `base` tại (x0, y0); ký tự '.' bỏ qua."""
    px = base.load()
    w, h = base.size
    for y, row in enumerate(parse(rows)):
        for x, ch in enumerate(row):
            if ch == ".":
                continue
            tx, ty = x0 + x, y0 + y
            if 0 <= tx < w and 0 <= ty < h:
                px[tx, ty] = rgba(ch)
    return base


def outlined(rows, edge="O"):
    """Thêm viền 1 px (8 hướng) quanh mọi ô không trong suốt; lưới nở thêm 1 ô mỗi phía."""
    rows = parse(rows)
    h, w = len(rows), len(rows[0])
    grid = [["."] * (w + 2) for _ in range(h + 2)]
    for y, row in enumerate(rows):
        for x, ch in enumerate(row):
            grid[y + 1][x + 1] = ch
    out = [r[:] for r in grid]
    for y in range(h + 2):
        for x in range(w + 2):
            if grid[y][x] != ".":
                continue
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    ny, nx = y + dy, x + dx
                    if 0 <= ny < h + 2 and 0 <= nx < w + 2 and grid[ny][nx] not in ".O":
                        out[y][x] = edge
    return ["".join(r) for r in out]


def from_mask(width, height, fn):
    """Dựng lưới từ hàm fn(x, y) -> ký tự."""
    return ["".join(fn(x, y) for x in range(width)) for y in range(height)]


def overlay(*layers):
    """Chồng các lưới cùng kích thước; lớp sau đè lớp trước (bỏ qua '.')."""
    rows = [list(r) for r in parse(layers[0])]
    for layer in layers[1:]:
        for y, row in enumerate(parse(layer)):
            for x, ch in enumerate(row):
                if ch != ".":
                    rows[y][x] = ch
    return ["".join(r) for r in rows]


def mirror(rows):
    return [r[::-1] for r in rows]


def flip(rows):
    return list(reversed(rows))


def rotate90(rows):
    """Xoay 90° theo chiều kim đồng hồ."""
    rows = parse(rows)
    h, w = len(rows), len(rows[0])
    return ["".join(rows[h - 1 - y][x] for y in range(h)) for x in range(w)]
