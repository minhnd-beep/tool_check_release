# Play Watch (GitHub Actions)

Tự kiểm tra Google Play mỗi 30 phút, app nào lên store thì bắn link Telegram **vào đúng nhóm của app đó**. Chạy trên GitHub Actions — không cần VPS, máy bạn tắt vẫn chạy.

## Cách hoạt động
- `packages.json`: map mỗi package → chat_id nhóm Telegram.
- `watch.py`: gọi trang Play Store. App chưa lên = HTTP 404, đã lên = 200. Đổi 404→200 thì bắn Telegram (chỉ 1 lần).
- `state.json`: nhớ app nào đã báo. Actions tự commit lại sau mỗi lần chạy.
- `.github/workflows/play-watch.yml`: đặt lịch cron.

---

## Cài đặt (làm 1 lần)

### 1. Tạo bot Telegram
- Chat với **@BotFather** → `/newbot` → lấy **BOT_TOKEN**.
- **Add con bot này vào TỪNG nhóm** cần nhận thông báo (1 bot dùng chung cho mọi nhóm).

### 2. Lấy chat_id của từng nhóm
- Mở 1 tin bất kỳ trong nhóm, copy link dạng `https://t.me/c/2465402876/3434`.
- chat_id = `-100` + số ở giữa → ví dụ `2465402876` ⟶ **`-1002465402876`**.

### 3. Điền `packages.json`
```json
{
  "com.cashflow.money.budget.tracker": "-1002465402876",
  "com.app.khac":                       "-1009876543210"
}
```

### 4. Push lên GitHub
```bash
cd play_watch
git init
git add .
git commit -m "play watch"
git branch -M main
git remote add origin https://github.com/<user>/<repo>.git
git push -u origin main
```

### 5. Thêm Secret
Trên repo GitHub: **Settings → Secrets and variables → Actions → New repository secret**
- Name: `TG_BOT_TOKEN`
- Value: token của bot.

### 6. Chạy thử
Tab **Actions → play-watch → Run workflow** (nút bấm tay). Xem log. Lần đầu app chưa lên thì im; khi nào lên sẽ bắn vào nhóm.

---

## Chỉnh
- **Tần suất**: sửa dòng `cron` trong workflow. `*/30 * * * *` = 30 phút; `0 * * * *` = mỗi giờ.
- **Thêm app**: thêm dòng vào `packages.json`, commit, push.
- **Báo lại từ đầu 1 app**: sửa giá trị app đó trong `state.json` về `false` (hoặc xoá khỏi file), commit.

## Lưu ý
- Cron của GitHub đôi khi trễ vài phút khi server bận — bình thường, không ảnh hưởng việc release app.
- Tín hiệu dựa trên 404/200 ở store `gl=us`. Muốn check theo quốc gia khác sửa `GL` trong `watch.py`.
