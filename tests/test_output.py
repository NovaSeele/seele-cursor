"""Kiểm tra cấu trúc file đầu ra: python3 -m unittest discover tests"""

import io
import struct
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT))

from PIL import Image  # noqa: E402

import build as builder  # noqa: E402
from curfile import ani_bytes, cur_bytes  # noqa: E402
from cursors import build, scaled, scaled_hotspot  # noqa: E402


def read_chunks(data):
    """Duyệt các chunk RIFF, trả về [(tag, payload)]."""
    out, i = [], 0
    while i < len(data):
        tag, size = data[i:i + 4], struct.unpack("<I", data[i + 4:i + 8])[0]
        out.append((tag, data[i + 8:i + 8 + size]))
        i += 8 + size + (size % 2)
    return out


class CurTest(unittest.TestCase):
    def test_header_and_pixels(self):
        cursors = build()
        for size in builder.SIZES:
            for c in cursors:
                img = scaled(c.frames[0][0], size)
                data = cur_bytes([(img, scaled_hotspot(c.hotspot, size))])
                reserved, kind, count = struct.unpack("<HHH", data[:6])
                self.assertEqual((reserved, kind, count), (0, 2, 1))
                w, h, _, _, hx, hy, length, offset = struct.unpack("<BBBBHHII", data[6:22])
                self.assertEqual((w, h), (size, size))
                self.assertEqual((hx, hy), scaled_hotspot(c.hotspot, size))
                self.assertLess(hx, size)
                self.assertLess(hy, size)
                self.assertEqual(offset + length, len(data))
                bi_size, bi_w, bi_h, planes, bits = struct.unpack("<IiiHH", data[22:38])
                self.assertEqual((bi_size, bi_w, bi_h, planes, bits), (40, size, size * 2, 1, 32))
                decoded = Image.open(io.BytesIO(data)).convert("RGBA")
                self.assertEqual(decoded.tobytes(), img.convert("RGBA").tobytes(), c.file)

    def test_hotspot_on_visible_pixel_or_shape(self):
        # điểm click phải nằm trong khung và gần hình con trỏ (không rơi vào vùng đầu)
        for c in build():
            x, y = c.hotspot
            self.assertTrue(x < 16 or (x, y) == (15, 15), c.file)


class AniTest(unittest.TestCase):
    def test_structure(self):
        animated = [c for c in build() if c.animated]
        self.assertEqual({c.file for c in animated}, {"Working", "Busy"})
        for c in animated:
            frames = [(cur_bytes([(img, c.hotspot)]), j) for img, j in c.frames]
            data = ani_bytes(frames, title="t", artist="a")
            self.assertEqual(data[:4], b"RIFF")
            self.assertEqual(struct.unpack("<I", data[4:8])[0], len(data) - 8)
            self.assertEqual(data[8:12], b"ACON")
            chunks = dict()
            for tag, payload in read_chunks(data[12:]):
                key = tag + (payload[:4] if tag == b"LIST" else b"")
                chunks[key] = payload
            anih = struct.unpack("<9I", chunks[b"anih"])
            self.assertEqual(anih[0], 36)
            self.assertEqual(anih[1], len(c.frames))
            self.assertEqual(anih[2], len(c.frames))
            self.assertEqual(anih[8] & 1, 1)
            icons = read_chunks(chunks[b"LISTfram"][4:])
            self.assertEqual(len(icons), len(c.frames))
            for (tag, payload), (blob, _) in zip(icons, frames):
                self.assertEqual(tag, b"icon")
                self.assertEqual(payload, blob)


class InfTest(unittest.TestCase):
    def test_all_roles_point_to_existing_files(self):
        cursors = build()
        files = {c.file: c.filename for c in cursors}
        text = builder.install_inf(cursors, 32).decode("ascii")
        self.assertIn("\r\n", text)
        self.assertEqual(len(builder.ROLES), 17)
        for role, file in builder.ROLES:
            self.assertIn(file, files)
            self.assertIn(f'Cursors",{role},0x00020000', text)
        scheme_line = next(line for line in text.split("\r\n") if line.startswith('HKCU,"Control Panel\\Cursors\\Schemes"'))
        self.assertEqual(scheme_line.count("%10%"), 17)


if __name__ == "__main__":
    unittest.main()
