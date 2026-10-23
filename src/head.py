"""Đầu chibi Seele (死生之律者, tóc dài) và các lớp biểu cảm.

Đầu gốc 22×22. Biểu cảm chỉ thay vùng mắt/miệng: mỗi lớp là một lưới
12×6 phủ lên vùng mặt bắt đầu ở FACE_ORIGIN.
"""

from sprite import parse, stamp, to_image

HEAD_W = HEAD_H = 22

HEAD = parse([
    ".......OOOOOOOO.......",  # 0
    ".....OOHHHHHHHHOO.....",  # 1
    "....OHHhhhhhhhhHHO....",  # 2
    "...OHhhlllhhhhhhhHO...",  # 3
    "..OHhhlpphhhhhhhhhHO..",  # 4
    "..OHhhpphhhhhhhhhhHO..",  # 5
    ".OHhhhhhhhhhhhhhhhhHO.",  # 6
    ".OHhhhhhhhhhhhhhhhhHO.",  # 7
    ".OHhhhhSShhhhSShhhhHO.",  # 8
    ".OHhhhSSSShhSSSShhhHO.",  # 9
    ".OHhhSSSSSShSSSSShhHO.",  # 10
    ".OHhhSSSSSSSSSSSShhHO.",  # 11  vùng mặt: hàng 11-16, cột 5-16
    ".OHhhSSSSSSSSSSSShhHO.",  # 12
    ".OHhhSSSSSSSSSSSShhHO.",  # 13
    ".OHhhSSSSSSSSSSSShhHO.",  # 14
    ".OHhhsSSSSSSSSSSshhHO.",  # 15
    ".OHhhhsSSSSSSSSshhhHO.",  # 16
    "OHhphhhOsSSSSsOhhhphHO",  # 17
    "OHhphhhhOsSSsOhhhhphHO",  # 18
    "OHhphOSSSkkkkSSSOhphHO",  # 19
    "OHpOdDDDDDDDDDDDDdOpHO",  # 20
    ".OO.OOOOOOOOOOOOOO.OO.",  # 21
])

# Kẹp tóc bướm trắng xanh ở bên phải đầu, ruy băng trắng và viên đá xanh.
HAIRCLIP = parse([
    ".OO.OO.",
    "OWWOWWO",
    "OWBOBWO",
    ".OWVWO.",
    "..OWO..",
    "...OWO.",
    "....Oc.",
])
HAIRCLIP_ORIGIN = (15, 1)

FACE_ORIGIN = (5, 11)

# Lưới 12×6 (cột 5-16, hàng 11-16). '.' = giữ nguyên da.
EXPRESSIONS = {
    # mỉm cười bình thản
    "smile": [
        "OOOO....OOOO",
        ".wEe....wEe.",
        ".EEE....EEE.",
        "bElE....ElEb",
        ".....mm.....",
        "............",
    ],
    # tò mò: mắt tròn, miệng chữ o
    "curious": [
        ".OOO....OOO.",
        ".wEe....wEe.",
        ".EEE....EEE.",
        ".ElE....ElE.",
        "......m.....",
        "............",
    ],
    # nhắm mắt buồn ngủ
    "sleepy": [
        "............",
        "............",
        "OOOO....OOOO",
        "b...O..O...b",
        ".....mm.....",
        "............",
    ],
    # nhắm mắt khi chớp (khung động)
    "blink": [
        "............",
        "............",
        "OOOO....OOOO",
        "b..........b",
        ".....mm.....",
        "............",
    ],
    # cười tươi, há miệng
    "happy": [
        "............",
        "..O......O..",
        ".O.O....O.O.",
        "b..........b",
        "....OmmO....",
        ".....OO.....",
    ],
    # mếu, rưng rưng
    "teary": [
        ".O........O.",
        "..OOO..OOO..",
        ".wEe....wEe.",
        ".cEE....EEc.",
        ".c...mm...c.",
        "....m..m....",
    ],
    # tập trung: mí hạ nửa
    "focused": [
        "............",
        "OOOO....OOOO",
        ".EEe....EEe.",
        ".ElE....ElE.",
        ".....mm.....",
        "............",
    ],
    # đỏ mặt
    "blush": [
        "OOOO....OOOO",
        ".wEe....wEe.",
        ".EEE....EEE.",
        "bbbb....bbbb",
        ".....mm.....",
        "............",
    ],
    # quyết tâm: lông mày chéo, mắt hẹp
    "determined": [
        ".O........O.",
        "..OOO..OOO..",
        ".wEe....wEe.",
        ".ElE....ElE.",
        ".....OO.....",
        "............",
    ],
}


def head(expression="smile"):
    img = to_image(HEAD)
    stamp(img, HAIRCLIP, *HAIRCLIP_ORIGIN)
    stamp(img, EXPRESSIONS[expression], *FACE_ORIGIN)
    return img
