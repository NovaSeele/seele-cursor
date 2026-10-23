"""Ghi file con trỏ Windows: .cur (ảnh tĩnh) và .ani (RIFF ACON).

.cur dùng header kiểu ICO với type = 2; trường planes/bitcount của mỗi mục
chứa toạ độ điểm click. Ảnh lưu dạng BMP 32 bit BGRA (có alpha) kèm mặt nạ
AND 1 bit, chiều cao trong BITMAPINFOHEADER gấp đôi theo quy ước ICO.
"""

import struct


def _dib(img):
    img = img.convert("RGBA")
    w, h = img.size
    header = struct.pack("<IiiHHIIiiII", 40, w, h * 2, 1, 32, 0, 0, 0, 0, 0, 0)
    px = img.load()
    xor = bytearray()
    for y in range(h - 1, -1, -1):  # BMP lưu từ dưới lên
        for x in range(w):
            r, g, b, a = px[x, y]
            xor += bytes((b, g, r, a))
    row_bytes = ((w + 31) // 32) * 4
    mask = bytearray()
    for y in range(h - 1, -1, -1):
        row = bytearray(row_bytes)
        for x in range(w):
            if px[x, y][3] == 0:
                row[x // 8] |= 0x80 >> (x % 8)
        mask += row
    return header + bytes(xor) + bytes(mask)


def cur_bytes(images):
    """images: danh sách (Image, (hotspot_x, hotspot_y)); trả về nội dung .cur."""
    out = struct.pack("<HHH", 0, 2, len(images))
    blobs = [_dib(img) for img, _ in images]
    offset = 6 + 16 * len(images)
    for (img, (hx, hy)), blob in zip(images, blobs):
        w, h = img.size
        out += struct.pack("<BBBBHHII", w % 256, h % 256, 0, 0, hx, hy, len(blob), offset)
        offset += len(blob)
    return out + b"".join(blobs)


def _chunk(tag, data):
    pad = b"\0" if len(data) % 2 else b""
    return tag + struct.pack("<I", len(data)) + data + pad


def _list(kind, payload):
    return _chunk(b"LIST", kind + payload)


def ani_bytes(frames, title="", artist=""):
    """frames: danh sách (cur_bytes, jiffies). Mỗi khung là một file .cur đầy đủ."""
    n = len(frames)
    info = b""
    if title:
        info += _chunk(b"INAM", title.encode("ascii") + b"\0")
    if artist:
        info += _chunk(b"IART", artist.encode("ascii") + b"\0")
    body = b""
    if info:
        body += _list(b"INFO", info)
    rates = [j for _, j in frames]
    default_rate = rates[0]
    # cbSize, nFrames, nSteps, cx, cy, cBitCount, cPlanes, jifRate, flags (AF_ICON)
    body += _chunk(b"anih", struct.pack("<9I", 36, n, n, 0, 0, 0, 0, default_rate, 1))
    if any(r != default_rate for r in rates):
        body += _chunk(b"rate", struct.pack(f"<{n}I", *rates))
    body += _list(b"fram", b"".join(_chunk(b"icon", data) for data, _ in frames))
    return b"RIFF" + struct.pack("<I", len(body) + 4) + b"ACON" + body
