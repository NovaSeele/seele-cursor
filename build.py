"""Dựng bộ con trỏ Seele: python3 build.py

Đầu ra:
  dist/Seele-32/, dist/Seele-48/  .cur/.ani + install.inf (chuột phải → Install)
  preview/                        ảnh xem trước để duyệt
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))

from PIL import Image, ImageDraw  # noqa: E402

from curfile import ani_bytes, cur_bytes  # noqa: E402
from cursors import SIZE, build, scaled, scaled_hotspot  # noqa: E402

SIZES = (32, 48)
SCHEME = "Seele Pixel"
ARTIST = "NovaSeele"

# Thứ tự 17 vai trò trong chuỗi scheme của Windows và file tương ứng.
ROLES = [
    ("Arrow", "Normal"),
    ("Help", "Help"),
    ("AppStarting", "Working"),
    ("Wait", "Busy"),
    ("Crosshair", "Precision"),
    ("IBeam", "Text"),
    ("NWPen", "Handwriting"),
    ("No", "Unavailable"),
    ("SizeNS", "Vertical"),
    ("SizeWE", "Horizontal"),
    ("SizeNWSE", "Diagonal1"),
    ("SizeNESW", "Diagonal2"),
    ("SizeAll", "Move"),
    ("UpArrow", "Normal"),  # Alternate Select dùng lại #1
    ("Hand", "Link"),
    ("Pin", "Person"),  # Location Select dùng chung #9
    ("Person", "Person"),
]

PREVIEW_BG = (0x6A, 0x8B, 0xB5, 255)


def write_cursor(cursor, size, folder):
    hotspot = scaled_hotspot(cursor.hotspot, size)
    images = [(scaled(img, size), jiffies) for img, jiffies in cursor.frames]
    if cursor.animated:
        frames = [(cur_bytes([(img, hotspot)]), jiffies) for img, jiffies in images]
        data = ani_bytes(frames, title=f"{SCHEME} {cursor.title}", artist=ARTIST)
    else:
        data = cur_bytes([(images[0][0], hotspot)])
    (folder / cursor.filename).write_bytes(data)


def install_inf(cursors, size):
    files = {c.file: c.filename for c in cursors}
    name = f"{SCHEME} {size}"
    cur_dir = f"Cursors\\{name}"
    key = {role: f"%10%\\%CUR_DIR%\\%{file}%" for role, file in ROLES}
    lines = [
        f"; {name} cursor scheme. Right-click this file and choose Install.",
        f'; Then open Mouse Properties > Pointers, pick "{name}" and click Apply.',
        "",
        "[Version]",
        'signature="$CHICAGO$"',
        "",
        "[DefaultInstall]",
        "CopyFiles = Scheme.Cur",
        "AddReg    = Scheme.Reg",
        "",
        "[DestinationDirs]",
        'Scheme.Cur = 10,"%CUR_DIR%"',
        "",
        "[Scheme.Reg]",
        'HKCU,"Control Panel\\Cursors\\Schemes","%SCHEME_NAME%",,"'
        + ",".join(key[role] for role, _ in ROLES) + '"',
        'HKCU,"Control Panel\\Cursors",,0x00020000,"%SCHEME_NAME%"',
        'HKCU,"Control Panel\\Cursors","Scheme Source",0x00010001,1',
    ]
    lines += [f'HKCU,"Control Panel\\Cursors",{role},0x00020000,"{key[role]}"' for role, _ in ROLES]
    lines += ["", "[Scheme.Cur]"] + list(files.values())
    lines += ["", "[Strings]", f'CUR_DIR     = "{cur_dir}"', f'SCHEME_NAME = "{name}"']
    lines += [f'{file:<11} = "{filename}"' for file, filename in files.items()]
    # Windows đọc INF theo ANSI nên giữ toàn bộ nội dung ở ASCII.
    return ("\r\n".join(lines) + "\r\n").encode("ascii")


def preview_grid(cursors, scale=4, pad=6, marker=False):
    cell = SIZE * scale + pad * 2
    label_h = 14
    sheet = Image.new("RGBA", (cell * 5, (cell + label_h) * 3), PREVIEW_BG)
    draw = ImageDraw.Draw(sheet)
    for i, c in enumerate(cursors):
        col, row = i % 5, i // 5
        x0, y0 = col * cell, row * (cell + label_h)
        img = c.frames[0][0].resize((SIZE * scale, SIZE * scale), Image.NEAREST)
        sheet.alpha_composite(img, (x0 + pad, y0 + pad))
        if marker:
            hx, hy = c.hotspot
            bx, by = x0 + pad + hx * scale, y0 + pad + hy * scale
            draw.rectangle([bx, by, bx + scale - 1, by + scale - 1], fill=(255, 0, 64, 255))
        draw.text((x0 + pad, y0 + cell - 2), f"{c.number} {c.file}", fill=(255, 255, 255, 255))
    return sheet


def preview_actual(cursors, size):
    """Ảnh cỡ thật trên nền trắng, xám, đen để kiểm tra độ rõ của viền."""
    gap = 8
    bgs = [(255, 255, 255, 255), (128, 128, 128, 255), (0, 0, 0, 255)]
    w = len(cursors) * (size + gap) + gap
    sheet = Image.new("RGBA", (w, len(bgs) * (size + gap) + gap))
    for r, bg in enumerate(bgs):
        band = Image.new("RGBA", (w, size + gap), bg)
        sheet.alpha_composite(band, (0, r * (size + gap) + gap // 2))
        for i, c in enumerate(cursors):
            sheet.alpha_composite(scaled(c.frames[0][0], size), (gap + i * (size + gap), gap + r * (size + gap)))
    return sheet


def preview_gif(cursor, path, scale=4):
    frames, durations = [], []
    for img, jiffies in cursor.frames:
        bg = Image.new("RGBA", img.size, PREVIEW_BG)
        bg.alpha_composite(img)
        frames.append(bg.resize((SIZE * scale, SIZE * scale), Image.NEAREST).convert("P"))
        durations.append(round(jiffies * 1000 / 60))
    frames[0].save(path, save_all=True, append_images=frames[1:], duration=durations, loop=0)


def main():
    cursors = build()
    for size in SIZES:
        folder = ROOT / "dist" / f"Seele-{size}"
        folder.mkdir(parents=True, exist_ok=True)
        for old in folder.glob("*"):
            old.unlink()
        for c in cursors:
            write_cursor(c, size, folder)
        (folder / "install.inf").write_bytes(install_inf(cursors, size))

    out = ROOT / "preview"
    out.mkdir(exist_ok=True)
    preview_grid(cursors).save(out / "cursors.png")
    preview_grid(cursors, marker=True).save(out / "hotspots.png")
    for size in SIZES:
        preview_actual(cursors, size).save(out / f"actual-{size}.png")
    for c in cursors:
        if c.animated:
            preview_gif(c, out / f"{c.file.lower()}.gif")
    print("đã ghi dist/ và preview/")


if __name__ == "__main__":
    main()
