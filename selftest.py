# -*- coding: utf-8 -*-
"""
Self-test: dung token trong bien moi truong de gui 1 tin test vao Telegram.
Dung de kiem tra Secret TG_BOT_TOKEN tren GitHub Actions co dung khong.

  py selftest.py <chat_id> [topic_id]
"""
import os, sys, urllib.request, urllib.parse, urllib.error

TOKEN = os.environ.get("TG_BOT_TOKEN", "")
if not TOKEN:
    print("Thieu TG_BOT_TOKEN"); sys.exit(1)

chat_id = sys.argv[1]
thread_id = sys.argv[2] if len(sys.argv) > 2 else None

payload = {
    "chat_id": chat_id,
    "text": "✅ Self-test: GitHub Actions → Telegram OK. Secret hợp lệ.",
    "parse_mode": "HTML",
}
if thread_id and thread_id != "-":
    payload["message_thread_id"] = thread_id

data = urllib.parse.urlencode(payload).encode("utf-8")
try:
    r = urllib.request.urlopen(
        urllib.request.Request(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data=data),
        timeout=20,
    )
    print("Self-test OK", r.status)
except urllib.error.HTTPError as e:
    print("Self-test LOI:", e.read().decode())
    sys.exit(1)
