#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
命令行工具：查看 ChatGPT Codex token 使用额度
支持短期(5小时)与长期(7天)窗口显示，可选参数:
    --token : 手动传入 Bearer Token
    --watch : 每隔 N 秒自动刷新显示
"""

import requests
import sys
import time
import argparse
from datetime import timedelta
from rich.console import Console
try:
    from codex_usage.configs import AUTH_TOKEN  # 默认从配置文件读取
except ImportError:
    AUTH_TOKEN = None
    
console = Console()

URL = "https://chatgpt.com/backend-api/wham/usage"
HEADERS_TEMPLATE = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json",
}

def seconds_to_hms(seconds: int) -> str:
    td = timedelta(seconds=seconds)
    d = td.days
    h, remainder = divmod(td.seconds, 3600)
    m, _ = divmod(remainder, 60)
    if d: return f"{d}天 {h}小时"
    if h: return f"{h}小时 {m}分钟"
    if m: return f"{m}分钟"
    return "不到1分钟"

def progress_bar(percent, length=30):
    filled = int(length * percent / 100)
    bar = "█" * filled + "░" * (length - filled)
    return f"[{bar}] {percent:.1f}%"

def fetch_data(auth_token: str):
    headers = HEADERS_TEMPLATE.copy()
    headers["Authorization"] = auth_token

    resp = requests.get(URL, headers=headers)
    if resp.status_code != 200:
        console.print(f"[red]❌ 请求失败：HTTP {resp.status_code}[/red]")
        return None
    return resp.json()

def display_usage(data):
    plan = data.get("plan_type", "unknown")
    rl = data.get("rate_limit", {})

    short = rl.get("primary_window", {})
    long = rl.get("secondary_window", {})

    used_s = short.get("used_percent", 0)
    used_l = long.get("used_percent", 0)
    reset_s = short.get("reset_after_seconds", 0)
    reset_l = long.get("reset_after_seconds", 0)

    console.print(f"\n[bold cyan]💡 ChatGPT Codex 使用情况[/bold cyan]")
    console.print(f"账户类型: [bold green]{plan}[/bold green]\n")

    console.print("🔹 [bold yellow]短期窗口（5小时）[/bold yellow]")
    console.print(progress_bar(used_s))
    console.print(f"已用: {used_s:.1f}%  剩余: {100-used_s:.1f}%")
    console.print(f"额度将在 [bold]{seconds_to_hms(reset_s)}[/bold] 后重置。\n")

    console.print("🔹 [bold yellow]长期窗口（7天）[/bold yellow]")
    console.print(progress_bar(used_l))
    console.print(f"已用: {used_l:.1f}%  剩余: {100-used_l:.1f}%")
    console.print(f"额度将在 [bold]{seconds_to_hms(reset_l)}[/bold] 后重置。\n")

def main():
    parser = argparse.ArgumentParser(description="查看 ChatGPT Codex 使用额度")
    parser.add_argument("--token", type=str, help="手动传入 Bearer Token（会覆盖 configs.py 中的）")
    parser.add_argument("--watch", type=int, help="每隔 N 秒自动刷新显示额度")
    args = parser.parse_args()

    # 使用命令行 token > 配置文件 token
    token = args.token if args.token else AUTH_TOKEN

    # 检查 token
    if not token or not token.startswith("Bearer "):
        console.print("[red]错误：未找到有效的 Bearer Token。请使用 --token 或在 configs.py 中配置 AUTH_TOKEN。[/red]")
        sys.exit(1)

    # watch 模式
    if args.watch:
        interval = args.watch
        console.print(f"[cyan]进入持续监控模式，每 {interval} 秒刷新一次[/cyan]\n")
        try:
            while True:
                data = fetch_data(token)
                if data:
                    display_usage(data)
                time.sleep(interval)
        except KeyboardInterrupt:
            console.print("\n[yellow]已退出监控模式。[/yellow]")
    else:
        data = fetch_data(token)
        if data:
            display_usage(data)

if __name__ == "__main__":
    main()
