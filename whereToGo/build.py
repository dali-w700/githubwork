#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build.py —— 「石家庄周边游」项目的构建脚本（单一数据源）

数据源（唯一需要手工维护的文件）：
    attractions.json

自动产物：
    1) index.html 内嵌的 `const DATA = [...]` 数据块
       —— 页面双击即可打开，无需本地服务器
    2) attractions.csv（UTF-8 BOM，Excel 可直接双击打开）

用法：
    python build.py

以后要增删/修改景点，只改 attractions.json，再运行本脚本即可。
"""

import csv
import json
import re
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent
JSON_PATH = BASE / "attractions.json"
HTML_PATH = BASE / "index.html"
CSV_PATH = BASE / "attractions.csv"

# CSV 表头与字段对应关系（CSV 不含 isFree，它由页面内部根据 ticket 字段判断）
CSV_HEADERS = [
    "景点名称", "所在城市", "类型", "特色",
    "距离(km)", "自驾时长(约)", "建议游玩天数", "门票参考", "备注",
]


def fmt_drive(minutes):
    """把 JSON 里的分钟数格式化为 CSV 中的中文时长：15 -> 15分钟，72 -> 1.2小时。"""
    try:
        m = int(minutes)
    except (TypeError, ValueError):
        return str(minutes)
    if m < 60:
        return f"{m}分钟"
    hours = m / 60
    text = f"{hours:.1f}".rstrip("0").rstrip(".")
    return f"{text}小时"


def rebuild_html(data):
    """把 index.html 里的 `const DATA = [...]` 整块替换为根据 JSON 序列化的内容。"""
    html = HTML_PATH.read_text(encoding="utf-8")
    rows = [
        "  " + json.dumps(obj, ensure_ascii=False, separators=(",", ":"))
        for obj in data
    ]
    block = "const DATA = [\n" + ",\n".join(rows) + "\n];"

    pattern = re.compile(r"const DATA = \[.*?\n\];", re.S)
    new_html, count = pattern.subn(lambda _m: block, html, count=1)
    if count != 1:
        print("[ERROR] 未在 index.html 中找到 `const DATA = [...]` 数据块", file=sys.stderr)
        return False

    if new_html == html:
        print("[ok] index.html 的 DATA 块已是最新，无需改动")
    else:
        HTML_PATH.write_text(new_html, encoding="utf-8")
        print(f"[ok] 已根据 attractions.json 重新生成 index.html 的 DATA 块（{len(data)} 条）")
    return True


def rebuild_csv(data):
    """从 JSON 导出 CSV（UTF-8 BOM，Excel 友好）。"""
    with CSV_PATH.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(CSV_HEADERS)
        for obj in data:
            writer.writerow([
                obj.get("name", ""),
                obj.get("city", ""),
                obj.get("type", ""),
                obj.get("features", ""),
                obj.get("distance", ""),
                fmt_drive(obj.get("drive", "")),
                obj.get("days", ""),
                obj.get("ticket", ""),
                obj.get("note", ""),
            ])
    print(f"[ok] 已导出 attractions.csv（{len(data)} 条）")


def main():
    if not JSON_PATH.exists():
        print(f"[ERROR] 找不到数据源文件：{JSON_PATH}", file=sys.stderr)
        return 1

    try:
        data = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        print(f"[ERROR] attractions.json 不是合法 JSON：{exc}", file=sys.stderr)
        return 1

    if not isinstance(data, list):
        print("[ERROR] attractions.json 顶层必须是数组（[ ... ]）", file=sys.stderr)
        return 1

    print(f"[info] 读取数据源 attractions.json，共 {len(data)} 条景点")
    if not rebuild_html(data):
        return 1
    rebuild_csv(data)
    print("[done] 构建完成 ✅")
    return 0


if __name__ == "__main__":
    sys.exit(main())
