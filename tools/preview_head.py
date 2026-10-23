"""Xuất ảnh duyệt các biểu cảm: preview/expressions.png."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from PIL import Image  # noqa: E402

from head import EXPRESSIONS, HEAD_H, HEAD_W, head  # noqa: E402

BG = (0x6A, 0x8B, 0xB5, 255)
SCALE = 8
PAD = 2


def main():
    names = list(EXPRESSIONS)
    cell_w, cell_h = HEAD_W + PAD * 2, HEAD_H + PAD * 2
    sheet = Image.new("RGBA", (cell_w * len(names), cell_h), BG)
    for i, name in enumerate(names):
        sheet.alpha_composite(head(name), (i * cell_w + PAD, PAD))
    out = ROOT / "preview" / "expressions.png"
    out.parent.mkdir(exist_ok=True)
    sheet.resize((sheet.width * SCALE, sheet.height * SCALE), Image.NEAREST).save(out)
    print(out, ", ".join(names))


if __name__ == "__main__":
    main()
