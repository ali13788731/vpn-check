import os
import re
import base64
import asyncio
import random
from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.network import ConnectionTcpFull

# --- تنظیمات ---
api_id = int(os.environ.get("API_ID"))
api_hash = os.environ.get("API_HASH")
session_string = os.environ.get("SESSION_STRING")
CHANNELS = ['napsternetv', 'v2rayng_org', 'v2ray_outlineir'] # کانال‌های بیشتر برای نتیجه بهتر
LIMIT = 200

async def main():
    if not session_string:
        print("Error: SESSION_STRING not found.")
        return

    async with TelegramClient(StringSession(session_string), api_id, api_hash, connection=ConnectionTcpFull) as client:
        print("✅ Connected to Telegram")
        
        extracted_configs = []
        
        for channel in CHANNELS:
            print(f"📡 Scanning {channel}...")
            try:
                async for msg in client.iter_messages(channel, limit=LIMIT):
                    if msg.text:
                        # استخراج دقیق انواع پروتکل‌ها
                        found = re.findall(r'(vmess|vless|trojan|ss|tuic|hysteria2?)://[a-zA-Z0-9\-_@:/?=&%.#]+', msg.text)
                        for conf in found:
                            # پاکسازی کاراکترهای اضافی انتهای لینک
                            clean_conf = conf.split('\n')[0].split(' ')[0]
                            extracted_configs.append(clean_conf)
            except Exception as e:
                print(f"⚠️ Error in {channel}: {e}")

        # حذف تکراری‌ها
        unique_configs = list(set(extracted_configs))
        print(f"Total Unique Configs: {len(unique_configs)}")

        # ذخیره در فایل
        with open("sub.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(unique_configs))
            
        # ذخیره نسخه Base64 (برای ایمپورت راحت‌تر)
        encoded_content = base64.b64encode("\n".join(unique_configs).encode("utf-8")).decode("utf-8")
        with open("sub_b64.txt", "w", encoding="utf-8") as f:
            f.write(encoded_content)

if __name__ == '__main__':
    asyncio.run(main())
