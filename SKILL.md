---
name: wechat-desktop-sender
description: Windows WeChat desktop automation for opening chats and sending messages. Use when the user wants to open 微信桌面端, search a contact or group, send a message, or send the same message to multiple contacts/groups in serial batch mode. Best for direct desktop WeChat messaging workflows like 文件传输助手 testing, one-to-one outreach, and串行群发. Not for browser WeChat,朋友圈 scraping, or reliable historical-message forwarding.
---

# wechat-desktop-sender

Use this skill for **Windows 微信桌面端发消息** workflows.

## What this skill provides

Bundled scripts:

- `scripts/wechat_send.py` — formal single-send command entry
- `scripts/wechat_send_hello.py` — core implementation (open WeChat, search chat, send, verify)
- `scripts/wechat_send_batch.py` — serial batch sender for multiple contacts/groups

## Quick start

Install dependencies:

```bash
pip install pywinauto pyperclip psutil pywin32 pillow pytesseract
```

> `pytesseract` is optional. Install it only if OCR verification is needed.

## Single send

```bash
python scripts/wechat_send.py --to "文件传输助手" --message "你好"
```

Useful flags:

```bash
python scripts/wechat_send.py --to "李义" --message "我是龙虾Koi，打个招呼。" --verify-title
python scripts/wechat_send.py --to "文件传输助手" --message "OCR测试" --ocr-verify
```

## Serial batch send

```bash
python scripts/wechat_send_batch.py --to "张三,李四,文件传输助手" --message "晚上 8 点开会"
```

Or from file:

```bash
python scripts/wechat_send_batch.py --contacts-file contacts.txt --message "晚上 8 点开会"
```

## Recommended workflow

1. Ensure WeChat desktop is logged in
2. Test on `文件传输助手` first
3. Use single-send for one contact/group
4. Use batch-send for serial outreach
5. Check `wechat_automation_logs/` for logs and summaries

## Verification model

Current verification layers:

1. UI element location succeeded
2. Message was sent through the input box
3. Window text verification checks whether the message text appears in current WeChat window
4. Optional OCR verification if `--ocr-verify` is enabled and OCR deps are installed

Treat this as **practical desktop automation**, not a cryptographic delivery guarantee.

## Boundaries

Do not claim support for these unless separately extended:

- Moments / 朋友圈 scraping
- Reliable historical message forwarding
- Multi-window true parallel sending
- Full desktop social graph extraction

## Files and outputs

By default, scripts create logs under:

```text
wechat_automation_logs/
```

Outputs may include:

- run logs
- failure screenshots
- control-tree dumps
- batch summary JSON files

## When to read more

For detailed CLI usage and arguments, read:

- `references/single-send.md`
- `references/batch-send.md`
