# -*- coding: utf-8 -*-
"""
Gui tin "dang theo doi" vao 1 topic Telegram (dung khi dang ky app moi).
Token doc tu bien moi truong TG_BOT_TOKEN (khong ghi token vao file).

Dung:
  py notify_start.py <chat_id> <topic_id|-> <package>
Vi du:
  py notify_start.py -1003488220919 4268 com.dailyspend.budget.expense.tracker
  py notify_start.py -1003488220919 -   com.app.khong.co.topic
"""
import os, sys, urllib.request, urllib.parse, urllib.error

TOKEN = os.environ.get("TG_BOT_TOKEN", "")
if not TOKEN:
    print("Thieu TG_BOT_TOKEN trong bien moi truong.")
    sys.exit(1)

chat_id   = sys.argv[1]
thread_id = sys.argv[2]
package   = sys.argv[3]

text = (
    "🔔 <b>Đang theo dõi</b>\n"
    f"<code>{package}</code>\n"
    "App lên Google Play sẽ báo link ngay tại đây."
)

payload = {"chat_id": chat_id, "text": text, "parse_mode": "HTML"}
if thread_id and thread_id != "-":
    payload["message_thread_id"] = thread_id

data = urllib.parse.urlencode(payload).encode("utf-8")
try:
    r = urllib.request.urlopen(
        urllib.request.Request(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data=data),
        timeout=20,
    )
    print("OK", r.status)
except urllib.error.HTTPError as e:
    print("LOI", e.read().decode())
