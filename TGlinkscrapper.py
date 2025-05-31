from pyrogram import Client
import re
import time
import os

# Your Info
api_id = My Api ID
api_hash = "My hash"
phone_number = "My number"

# Telegram Client
client = Client("link_scraper", api_id=api_id, api_hash=api_hash, phone_number=phone_number)

# URL search regex
url_pattern = re.compile(r"https?://[^\s]+")

# User input
channel_username = input("Enter the channel username: ").strip().lstrip("@")

# Start connection
with client:
    try:
        chat = client.get_chat(channel_username)
        channel_id = chat.id
        channel_title = chat.title.replace(" ", "_")
        print(f"[+] Channel found: {channel_title}")
    except Exception as e:
        print(f"[!] Error loading channel: {e}")
        exit()

    save_path = f"/storage/emulated/0/YouTube/Telegram/link_{channel_title}.txt"
    all_links = set()
    count = 0

    for message in client.get_chat_history(channel_id):
        texts = [message.text, message.caption]
        for content in texts:
            if content:
                urls = url_pattern.findall(content)
                all_links.update(urls)

        count += 1
        if count % 100 == 0:
            print(f"[link_scraper] Scanned {count} messages, taking a 5-second break...")
            time.sleep(5)

    # Save links to file
    if all_links:
        with open(save_path, "w", encoding="utf-8") as f:
            for i, link in enumerate(sorted(all_links), start=1):
                f.write(f"{i}. {link}\n")
        print(f"[✓] {len(all_links)} links saved: {save_path}")
    else:
        print("[!] No links found.")