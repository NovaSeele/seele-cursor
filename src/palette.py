"""Bảng màu, mỗi màu gắn với một ký tự dùng trong sprite dạng chuỗi.

Màu lấy theo docs/DESIGN.md; các màu đánh dấu "thêm" không có trong bảng gốc.
"""

PALETTE = {
    ".": None,  # trong suốt
    "O": "#2a2440",  # viền ngoài
    "H": "#3f3a53",  # tóc tối
    "h": "#4b3956",  # tóc trung
    "p": "#913c8f",  # tóc ánh tím
    "l": "#908bc1",  # tóc tím nhạt
    "W": "#eff8fd",  # kẹp tóc trắng
    "B": "#b0bbe4",  # kẹp tóc xanh nhạt
    "V": "#886baa",  # kẹp tóc tím
    "S": "#faf5f0",  # da
    "s": "#ebe1de",  # bóng da
    "E": "#74637d",  # mắt
    "e": "#4a364b",  # mắt tối
    "w": "#efeded",  # chấm sáng mắt
    "D": "#fffcf4",  # váy
    "d": "#b4b2bd",  # bóng váy
    "k": "#65616b",  # nét váy tối / choker
    # thêm
    "m": "#c0626e",  # miệng
    "b": "#f4b9c1",  # má hồng
    "X": "#ffffff",  # thân mũi tên
    "x": "#c9d3ee",  # bóng mũi tên
    "c": "#6fc3f0",  # tinh thể / nước mắt / dấu "?"
    "C": "#3a8fd0",  # tinh thể đậm
    "r": "#e0404a",  # biển cấm
    "R": "#9c2230",  # biển cấm đậm
    "i": "#ff8fb3",  # trái tim
    "I": "#d94f80",  # trái tim đậm
    "y": "#f2d48a",  # cát đồng hồ
    "Y": "#c99a3e",  # khung đồng hồ cát
}


def rgba(ch):
    """Trả về bộ (r, g, b, a) cho một ký tự bảng màu."""
    value = PALETTE[ch]
    if value is None:
        return (0, 0, 0, 0)
    return (int(value[1:3], 16), int(value[3:5], 16), int(value[5:7], 16), 255)
