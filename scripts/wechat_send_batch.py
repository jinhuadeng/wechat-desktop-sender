import argparse
import json
import logging
import time
from datetime import datetime
from pathlib import Path

from wechat_send_hello import (
    DEFAULT_LOG_DIR,
    connect_wechat_window,
    ensure_wechat,
    open_chat,
    send_message,
    setup_logging,
)


def parse_args():
    parser = argparse.ArgumentParser(description="微信串行批量发送")
    parser.add_argument("--to", help="逗号分隔的联系人/群聊列表，例如 张三,李四,文件传输助手")
    parser.add_argument("--contacts-file", help="联系人文件路径，每行一个")
    parser.add_argument("--message", required=True, help="要发送的消息")
    parser.add_argument("--delay", type=float, default=1.5, help="每步 UI 操作后的等待秒数")
    parser.add_argument("--between", type=float, default=1.0, help="每个联系人之间的等待秒数")
    parser.add_argument("--log-dir", default=str(DEFAULT_LOG_DIR), help="日志与结果输出目录")
    parser.add_argument("--verify-title", action="store_true", help="校验窗口标题里是否包含聊天名")
    parser.add_argument("--stop-on-error", action="store_true", help="遇到发送失败时立即停止")
    return parser.parse_args()


def load_contacts(args):
    contacts = []
    if args.to:
        contacts.extend([x.strip() for x in args.to.split(",") if x.strip()])
    if args.contacts_file:
        path = Path(args.contacts_file)
        if not path.exists():
            raise FileNotFoundError(f"联系人文件不存在: {path}")
        contacts.extend([line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip()])

    seen = set()
    deduped = []
    for c in contacts:
        if c not in seen:
            seen.add(c)
            deduped.append(c)
    if not deduped:
        raise ValueError("没有可发送的联系人，请提供 --to 或 --contacts-file")
    return deduped


def save_summary(log_dir: Path, results):
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    out = log_dir / f"wechat-batch-summary-{ts}.json"
    out.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    logging.info("批量发送结果已保存: %s", out)
    return out


def main():
    args = parse_args()
    log_dir = Path(args.log_dir)
    log_file = setup_logging(log_dir)
    contacts = load_contacts(args)

    logging.info("日志文件: %s", log_file)
    logging.info("批量发送启动，联系人数量: %s", len(contacts))
    logging.info("联系人列表: %s", contacts)

    ensure_wechat()
    win = connect_wechat_window()

    results = []
    for idx, contact in enumerate(contacts, start=1):
        item = {
            "contact": contact,
            "success": False,
            "verified": False,
            "error": None,
            "index": idx,
        }
        try:
            logging.info("[%s/%s] 开始发送给: %s", idx, len(contacts), contact)
            open_chat(win, contact, args.delay, args.verify_title)
            verified, _texts = send_message(win, args.message, args.delay)
            item["success"] = True
            item["verified"] = bool(verified)
            logging.info("[%s/%s] 完成: %s | verified=%s", idx, len(contacts), contact, verified)
        except Exception as e:
            item["error"] = str(e)
            logging.exception("[%s/%s] 发送失败: %s", idx, len(contacts), contact)
            if args.stop_on_error:
                results.append(item)
                save_summary(log_dir, results)
                raise
        results.append(item)
        if idx < len(contacts):
            time.sleep(args.between)

    success_count = sum(1 for x in results if x["success"])
    verified_count = sum(1 for x in results if x["verified"])
    logging.info("批量发送完成: success=%s/%s, verified=%s/%s", success_count, len(results), verified_count, len(results))
    save_summary(log_dir, results)


if __name__ == "__main__":
    main()
