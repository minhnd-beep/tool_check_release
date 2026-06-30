#!/usr/bin/env python3
"""
Kiem tra Google Play va bao Telegram khi app da len store.
Chay 1 lan moi lan duoc goi (GitHub Actions cron lo phan dat lich).

Khong can pip install gi - chi dung thu vien chuan.
"""

import json
import os
import urllib.request
import urllib.parse
import urllib.error

# Token Telegram lay tu GitHub Secrets (bien moi truong)
BOT_TOKEN = os.environ.get("TG_BOT_TOKEN", "")

HERE = os.path.dirname(os.path.abspath(__file__))
PACKAGES_FILE = os.path.join(HERE, "packages.json")   # { "com.xxx": "-100...chat_id..." }
STATE_FILE    = os.path.join(HERE, "state.json")       # nho app nao da bao roi

GL = "us"          # quoc gia store kiem tra
HL = "en"
TIMEOUT = 20
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
      "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36")


def load_json(path, default):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return default


def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def is_live(package):
    """True neu trang Play Store cua app ton tai (HTTP 200)."""
    qs = urllib.parse.urlencode({"id": package, "gl": GL, "hl": HL})
    url = "https://play.google.com/store/apps/details?" + qs
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            return resp.status == 200
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return False
        print(f"  [warn] {package}: HTTP {e.code}")
        return False
    except Exception as e:
        print(f"  [warn] {package}: {e}")
        return False


def parse_target(value):
    """value co the la 'chat_id' hoac 'chat_id:topic_id' (nhom co Topics)."""
    s = str(value).strip()
    if ":" in s:
        chat_id, thread_id = s.split(":", 1)
        return chat_id.strip(), thread_id.strip()
    return s, None


def send_telegram(chat_id, text, thread_id=None):
    if not BOT_TOKEN:
        print("  [error] Thieu TG_BOT_TOKEN")
        return False
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML",
    }
    if thread_id:
        payload["message_thread_id"] = thread_id   # ban vao dung topic
    data = urllib.parse.urlencode(payload).encode()
    req = urllib.request.Request(url, data=data)
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            return resp.status == 200
    except Exception as e:
        print(f"  [telegram error] chat {chat_id}: {e}")
        return False


def main():
    packages = load_json(PACKAGES_FILE, {})
    state = load_json(STATE_FILE, {})

    if not packages:
        print("packages.json rong - them package vao truoc.")
        return

    for pkg, target in packages.items():
        chat_id, thread_id = parse_target(target)
        live = is_live(pkg)
        was_live = bool(state.get(pkg, False))
        print(f"  {pkg}: {'LIVE' if live else 'chua len'}")

        if live and not was_live:
            link = f"https://play.google.com/store/apps/details?id={pkg}"
            msg = (f"✅ <b>Đã lên Google Play</b>\n"
                   f"<code>{pkg}</code>\n{link}")
            if send_telegram(chat_id, msg, thread_id):
                print(f"  -> da bao {chat_id}"
                      + (f" topic {thread_id}" if thread_id else "") + f": {pkg}")

        state[pkg] = live

    save_json(STATE_FILE, state)
    print("Xong.")


if __name__ == "__main__":
    main()
