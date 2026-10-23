# Thiết kế: bộ con trỏ pixel Seele (HI3)

Ghi chú soạn ngày 2026-10-23, trước khi bắt đầu vẽ. File này là nguồn tham chiếu cho mọi phiên làm việc, kể cả phiên trên cloud.

## Nguyên tắc

- **Thiết kế riêng.** Bố cục lấy ý tưởng từ các bộ con trỏ pixel kiểu "đầu chibi cạnh mũi tên" (ví dụ của họa sĩ 乱涂乱画ben). Không đồ lại sprite của ai, không xóa watermark "sample" trên ảnh xem trước của người khác.
- Chỉ dùng cá nhân, phi thương mại.

## Nhân vật

Tạo hình mục tiêu là **死生之律者 (Herrscher of Rebirth)**, bản tóc dài. Bản mặc định và bản 彼岸双生 tóc ngắn nên không dùng làm mẫu dáng đầu.

Những nét phải giữ để vẫn nhận ra Seele khi đầu chỉ khoảng 24 px:

- Tóc dài thẳng màu chàm/xanh navy đậm, quá vai; lớp tóc bên trong ánh tím; tóc mai ôm mặt; vài sợi tóc tơ.
- Kẹp tóc hình bướm/hoa màu trắng xanh nhạt ở một bên đầu, kèm sợi ruy băng trắng mảnh và viên đá xanh nhỏ.
- Mắt to màu tím lam nhạt, có chấm sáng trắng; nét mặt hiền, hơi rụt rè.
- Váy trắng trễ vai, vòng cổ (choker) tối màu, da trắng.
- Họa tiết phụ: bướm xanh, hoa trắng, mảnh tinh thể băng xanh.

### Bảng màu

Lấy mẫu từ ảnh chân dung gốc `死生之律者头像.png`; khi dựng dải màu pixel thì chỉnh lại cho hợp.

| Vùng | Màu |
|---|---|
| Tóc tối | `#3f3a53` |
| Tóc trung | `#4b3956` |
| Tóc ánh tím | `#913c8f` |
| Tóc tím nhạt | `#908bc1` |
| Kẹp tóc trắng | `#eff8fd` |
| Kẹp tóc xanh nhạt | `#b0bbe4` |
| Kẹp tóc tím | `#886baa` |
| Da | `#faf5f0` |
| Bóng da | `#ebe1de` |
| Mắt | `#74637d`, `#4a364b` |
| Chấm sáng mắt | `#efeded` |
| Váy | `#fffcf4` |
| Bóng váy | `#b4b2bd` |
| Nét váy tối | `#65616b` |
| Viền ngoài | `#2a2440` (đề xuất) |
| Nền ô xem trước | khoảng `#6a8bb5` (chỉ dùng cho ảnh preview; con trỏ thật có nền trong suốt) |

### Ảnh tham khảo

Nguồn: wiki Bilibili HI3, trang 希儿·芙乐艾.

- Ảnh 死生之律者 2160 px: https://patchwiki.biligame.com/images/bh3/0/04/ffbb4k5uq3k6h6csvixnwxy3kk1d1lc.png
- Ảnh chân dung 140×120: https://patchwiki.biligame.com/images/bh3/b/b9/od2ik8vyftflo9ohhupjny3okn63idk.png
- Tìm thêm file qua `https://wiki.biligame.com/bh3/api.php` với `generator=search&gsrnamespace=6`. Wiki chặn tạm (HTTP 567) nếu gọi dồn dập.

## Bố cục và kích thước

- Khung gốc 32×32. Bản 48×48 vẽ lại hoặc phóng nearest-neighbour ×1.5 rồi sửa tay.
- Hình con trỏ (mũi tên, I-beam…) ở góc trên trái; đầu chibi (khoảng 22×22) ở góc dưới phải để không che điểm click.
- Viền tối 1 px quanh mọi thứ để nhìn rõ trên cả nền trắng lẫn nền đen.

## 15 con trỏ

| # | Vai trò Windows | Hình con trỏ | Biểu cảm Seele | Điểm click |
|---|---|---|---|---|
| 1 | Normal (Arrow) | Mũi tên trắng | Mỉm cười bình thản | (0,0) |
| 2 | Help | Mũi tên + "?" xanh | Nghiêng đầu tò mò | (0,0) |
| 3 | Working in background (AppStarting), `.ani` | Mũi tên + đồng hồ cát nhỏ | 4–8 khung: cát chảy / chớp mắt | (0,0) |
| 4 | Busy (Wait), `.ani` | Chỉ đồng hồ cát | Nhắm mắt buồn ngủ, "zZ" | Tâm |
| 5 | Text (IBeam) | I-beam | Đầu nhỏ | Tâm thanh I |
| 6 | Link (Hand) | Bàn tay chỉ | Cười tươi, há miệng | Đầu ngón tay |
| 7 | Unavailable (No) | Biển cấm đỏ | Mếu, rưng rưng | Tâm biển cấm |
| 8 | Handwriting (Pen) | Bút (hoặc cán lưỡi hái thu nhỏ) | Tập trung | Đầu bút |
| 9 | Person + Location | Trái tim hồng | Đỏ mặt | Tâm trái tim |
| 10 | Precision (Cross) | Dấu ngắm mảnh | Quyết tâm | Tâm |
| 11 | Move (SizeAll) | 4 mũi tên quanh tinh thể/bướm | Không có mặt | Tâm |
| 12 | Horizontal (SizeWE) | Mũi tên ngang | Không có mặt | Tâm |
| 13 | Vertical (SizeNS) | Mũi tên dọc | Không có mặt | Tâm |
| 14 | Diagonal 1 (SizeNWSE) | Mũi tên chéo ↖↘ | Không có mặt | Tâm |
| 15 | Diagonal 2 (SizeNESW) | Mũi tên chéo ↗↙ | Không có mặt | Tâm |

Windows có 17 vai trò con trỏ. File #9 dùng chung cho Person và Location (có từ Windows 10 1709); Alternate select dùng lại #1 hoặc một biến thể mũi tên chỉ lên.

## Thứ tự làm

1. Dựng bảng màu, vẽ một sprite đầu gốc và 5–6 lớp biểu cảm (chỉ thay mắt/miệng). Gửi duyệt, chỉnh 2–3 vòng.
2. Vẽ các hình con trỏ.
3. Ghép 15 ô và xuất ảnh xem trước dạng lưới 3×5.
4. Ghi `.cur`/`.ani` bằng Python, đặt đúng điểm click: `.cur` dùng header kiểu ICO (type = 2, hotspot nằm ở trường planes/bitcount); `.ani` dùng RIFF `ACON` (`anih`, `rate`, `LIST fram`).
5. Viết `install.inf` gán đủ 17 vai trò trong registry. Người dùng tự cài thử trên Windows (phiên cloud chạy Linux nên không thử cài được).

## Tiến độ

Cập nhật 2026-10-23 (phiên cloud). Phiên cloud không tải được ảnh tham khảo từ wiki Bilibili (proxy chặn), nên đầu Seele được vẽ theo mô tả và bảng màu ở trên.

- [x] Bước 1: đầu gốc 22×22 + 9 biểu cảm (`smile`, `curious`, `sleepy`, `blink`, `happy`, `teary`, `focused`, `blush`, `determined`). Bản nháp vòng 1, **chờ duyệt**: `preview/expressions.png`.
- [x] Bước 2: các hình con trỏ (`src/shapes.py`).
- [x] Bước 3: lưới 3×5 `preview/cursors.png`; `preview/hotspots.png` đánh dấu điểm click bằng ô đỏ; `preview/actual-32.png`, `actual-48.png` là cỡ thật trên nền trắng/xám/đen; `busy.gif`, `working.gif` là khung động.
- [x] Bước 4: `.cur` (BMP 32 bit có alpha + mặt nạ AND) và `.ani` (`anih`, `rate` khi các khung khác nhịp, `LIST fram`). Có test đọc ngược lại.
- [x] Bước 5: `install.inf` gán đủ 17 vai trò. **Chưa thử cài trên Windows.**

Còn lại:

- Duyệt đầu và biểu cảm, sửa 2–3 vòng.
- Bản 48 px đang phóng nearest-neighbour ×1.5 nên viền chỗ dày 1 px, chỗ 2 px; cần sửa tay hoặc vẽ riêng.
- #5 Text đang dùng đầu cỡ thường; thiết kế ghi "đầu nhỏ" nhưng chưa vẽ bản nhỏ.
- Alternate select (UpArrow) đang dùng lại #1.
