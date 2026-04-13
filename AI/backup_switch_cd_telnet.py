#!/usr/bin/env python3
"""
Backup switch configurations over Telnet.

Copyright (c) 2026 Leo Yuan.
Created with GitHub Copilot in Visual Studio Code.
Model: GPT-5.3-Codex.

依赖与前提:
需要 Python 包 pexpect 可用。
系统需有 telnet 命令（脚本会检查 shutil.which("telnet")）。
Telnet 在网络上可达目标交换机且凭证正确。


Usage:
    python3 backup_switch_configs.py --swinfo swinfo.txt --out-dir .
    python backup_switch_configs.py --swinfo swinfo.txt --out-dir .
    python3 backup_switch_configs.py --swinfo swinfo.txt --out-dir . --default-password "YOUR_PASSWORD"
    pip install pexpect

Linux example (env var):
    export SWITCH_PASSWORD="YOUR_PASSWORD"
    python3 backup_switch_configs.py --swinfo swinfo.txt --out-dir .

Windows PowerShell example (env var):
    $env:SWITCH_PASSWORD="YOUR_PASSWORD"
    python backup_switch_configs.py --swinfo swinfo.txt --out-dir .

    
######    
中文用法:
    python3 backup_switch_configs.py --swinfo swinfo.txt --out-dir .
    python backup_switch_configs.py --swinfo swinfo.txt --out-dir .
    python3 backup_switch_configs.py --swinfo swinfo.txt --out-dir . --default-password "你的密码"

Linux 环境变量示例:
    export SWITCH_PASSWORD="你的密码"
    python3 backup_switch_configs.py --swinfo swinfo.txt --out-dir .

Windows PowerShell 环境变量示例:
    $env:SWITCH_PASSWORD="你的密码"
    python backup_switch_configs.py --swinfo swinfo.txt --out-dir .
#######
    


Input file format (netconf/swinfo.txt):

#telnet
position,model,ip,password
position,model,ip
...

Only entries under #telnet are processed until the next section header.
If password is missing on a line, the script uses --default-password or
SWITCH_PASSWORD from environment.
"""

from __future__ import annotations

import argparse
import datetime as dt
import importlib
import os
import re
import shutil
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

try:
    pexpect = importlib.import_module("pexpect")
except ModuleNotFoundError:
    pexpect = None


MODEL_COMMANDS: Dict[str, List[str]] = {
    "h3c": ["dis version", "dis current", "dis vlan", "quit"],
    "huawei": ["dis version", "dis current", "dis vlan", "quit"],
    "cisco": ["enable", "show ver", "show run", "exit", "exit"],
}

# Prompt detection: require a hostname (or optional `sysname ` prefix) before
# the `#` so we don't mistake a lone `#` inside config for the CLI prompt.
# Accept optional angle brackets around the prompt and optional digits after `#`.
PROMPT_PATTERN = r"(?mi)^(?:sysname\s+)?(?:<[^>]+>|[A-Za-z0-9\-_.]+#\d*)\s?$"
MORE_PATTERNS = [r"--More--", r"---- More ----", r"<--- More --->", r"\[More\]"]


def _sanitize_output(s: str) -> str:
    """Remove ANSI escapes and control characters that clutter outputs."""
    if not s:
        return s
    # Normalize line endings from network devices.
    # Some outputs contain "\r\r\n"; treat that as a single newline.
    s = re.sub(r"\r+\n", "\n", s)
    # A lone carriage return is often cursor-control, not a real newline.
    s = s.replace("\r", "")
    # remove common ANSI CSI sequences like ESC[...m or ESC[...K
    s = re.sub(r"\x1b\[[0-9;?]*[A-Za-z]", "", s)
    # remove overstrike patterns produced with backspace (e.g. "x\b")
    while True:
        new_s = re.sub(r".\x08", "", s)
        if new_s == s:
            break
        s = new_s
    # remove any remaining backspace characters
    s = s.replace("\x08", "")
    # remove pager hints that may still appear in captured output
    s = re.sub(r"(?mi)^\s*(?:--More--|---- More ----|<--- More --->|\[More\])\s*$", "", s)
    # strip other C0 control chars except newline and tab
    s = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]", "", s)
    return s


@dataclass
class SwitchInfo:
    position: str
    model: str
    ip: str
    password: str


def parse_swinfo(swinfo_path: Path, default_password: str) -> List[SwitchInfo]:
    entries: List[SwitchInfo] = []
    in_telnet = False

    with swinfo_path.open("r", encoding="utf-8") as f:
        for raw in f:
            line = raw.strip()
            if not line:
                continue
            if line.startswith("#"):
                in_telnet = line.lower() == "#telnet"
                continue
            if not in_telnet:
                continue

            parts = [p.strip() for p in line.split(",")]
            if len(parts) < 3:
                print(f"[WARN] Skip invalid line: {line}")
                continue

            position, model, ip = parts[0], parts[1].lower(), parts[2]
            password = parts[3] if len(parts) >= 4 and parts[3] else default_password

            if model not in MODEL_COMMANDS:
                print(f"[WARN] Unsupported model '{model}' at {ip}, skipped")
                continue
            if not password:
                print(f"[WARN] No password for {position}/{model}/{ip}, skipped")
                continue

            entries.append(SwitchInfo(position, model, ip, password))

    return entries


def _read_until_any(
    child: Any, patterns: List[str], timeout: float = 8.0
) -> Tuple[str, Optional[str]]:
    if pexpect is None:
        return "", None
    try:
        idx = child.expect(patterns + [pexpect.TIMEOUT, pexpect.EOF], timeout=timeout)
    except Exception:
        return "", None

    data = (child.before or "")
    if isinstance(child.after, str):
        data += child.after

    if idx < len(patterns):
        return data, patterns[idx]
    if idx == len(patterns) + 1:
        data += "\n[connection-closed-by-remote]\n"
    return data, None


def _read_command_output(child: Any, timeout: float = 12.0) -> str:
    if pexpect is None:
        return ""
    end = time.time() + timeout
    data = ""
    while time.time() < end:
        try:
            idx = child.expect(MORE_PATTERNS + [PROMPT_PATTERN, pexpect.TIMEOUT, pexpect.EOF], timeout=1.0)
            part = child.before or ""
            if isinstance(child.after, str):
                part += child.after
            data += part
            if idx < len(MORE_PATTERNS):
                try:
                    child.send("\x20")
                except Exception:
                    child.send(" ")
                data += "\n[auto-send-space-for-more]\n"
                continue
            if idx == len(MORE_PATTERNS):
                # Prompt found, command output finished.
                break
            if idx == len(MORE_PATTERNS) + 1:
                # TIMEOUT for this 1s slice, keep reading until overall timeout.
                continue
            if idx == len(MORE_PATTERNS) + 2:
                data += "\n[connection-closed-by-remote]\n"
                break
        except Exception as exc:
            data += f"\n[read-error] {type(exc).__name__}: {exc}\n"
            break
    return data


def backup_one(sw: SwitchInfo, out_dir: Path, timeout: int) -> Tuple[bool, Path, str, float]:
    start_ts = time.perf_counter()
    now = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{sw.position}_{sw.model}_{sw.ip}_{now}.txt"
    out_file = out_dir / filename

    transcript = []
    transcript.append(f"=== Backup Start: {dt.datetime.now().isoformat()} ===")
    transcript.append(f"position={sw.position}, model={sw.model}, ip={sw.ip}")

    try:
        child = pexpect.spawn(
            "telnet",
            [sw.ip],
            encoding="utf-8",
            codec_errors="replace",
            timeout=timeout,
        )
        time.sleep(0.5)

        banner = child.before or ""
        if banner:
            transcript.append("\n--- Banner ---\n" + _sanitize_output(banner))

        login_data, matched = _read_until_any(
            child,
            [r"(?i)username[: ]*$", r"(?i)login[: ]*$", r"(?i)password[: ]*$", PROMPT_PATTERN],
            timeout=8.0,
        )
        if login_data:
            transcript.append("\n--- Login Prompt ---\n" + _sanitize_output(login_data))

        if matched and re.search(r"username|login", matched, flags=re.IGNORECASE):
            username = os.environ.get("SWITCH_USERNAME", "")
            child.sendline(username)
            data2, _ = _read_until_any(child, [r"(?i)password[: ]*$"], timeout=5.0)
            if data2:
                transcript.append("\n--- After Username ---\n" + _sanitize_output(data2))
            child.sendline(sw.password)
        elif matched and re.search(r"password", matched, flags=re.IGNORECASE):
            child.sendline(sw.password)
        else:
            # If prompt is already available, continue. If not, still attempt password once.
            child.sendline(sw.password)

        post_login = _read_command_output(child, timeout=6.0)
        if post_login:
            transcript.append("\n--- Post Login ---\n" + _sanitize_output(post_login))

        # Disable paging on VRP-based devices (Huawei / H3C) to ensure full
        # command output is returned without "--More--" pauses.
        if sw.model in ("huawei", "h3c"):
            try:
                # H3C/Comware may use a different paging command than Huawei.
                if sw.model == "h3c":
                    child.sendline("screen-length 0")
                    screen_out = _read_command_output(child, timeout=6.0)
                    # if unrecognized, try the Huawei variant as fallback
                    if "Unrecognized command" in screen_out or "Unrecognized" in screen_out:
                        child.sendline("screen-length 0 temporary")
                        screen_out = _read_command_output(child, timeout=6.0)
                else:
                    child.sendline("screen-length 0 temporary")
                    screen_out = _read_command_output(child, timeout=6.0)
                transcript.append("\n$ screen-length (disable paging)\n" + _sanitize_output(screen_out))
            except Exception:
                # non-fatal: continue even if disabling paging failed
                transcript.append("\n[WARN] Failed to disable paging (continuing)\n")

        commands = MODEL_COMMANDS[sw.model]

        for cmd in commands:
            if sw.model == "cisco" and cmd == "enable":
                child.sendline("enable")
                enable_prompt, _ = _read_until_any(child, [r"(?i)password[: ]*$", r"#\s*$"], timeout=4.0)
                transcript.append("\n$ enable\n" + _sanitize_output(enable_prompt))
                if re.search(r"password", enable_prompt, flags=re.IGNORECASE):
                    child.sendline(sw.password)
                    enable_done = _read_command_output(child, timeout=4.0)
                    transcript.append(_sanitize_output(enable_done))
                continue

            child.sendline(cmd)
            # 'dis current' may produce very long output; allow more time.
            cmd_timeout = 120.0 if cmd.lower().startswith("dis current") else 20.0
            output = _read_command_output(child, timeout=cmd_timeout)
            transcript.append(f"\n$ {cmd}\n" + _sanitize_output(output))

        child.close(force=True)
        elapsed = time.perf_counter() - start_ts
        transcript.append(f"elapsed_seconds={elapsed:.2f}")
        transcript.append(f"\n=== Backup End: {dt.datetime.now().isoformat()} ===")

        out_file.write_text("\n".join(transcript), encoding="utf-8", errors="replace")
        return True, out_file, "ok", elapsed

    except Exception as exc:
        elapsed = time.perf_counter() - start_ts
        transcript.append(f"\n[ERROR] {type(exc).__name__}: {exc}")
        transcript.append(f"elapsed_seconds={elapsed:.2f}")
        transcript.append(f"\n=== Backup End (Failed): {dt.datetime.now().isoformat()} ===")
        out_file.write_text("\n".join(transcript), encoding="utf-8", errors="replace")
        return False, out_file, str(exc), elapsed


def main() -> int:
    if pexpect is None:
        print("[ERROR] Missing dependency: pexpect")
        print("[HINT] Install it with: pip install pexpect")
        return 4
    if shutil.which("telnet") is None:
        print("[ERROR] 'telnet' command not found in PATH")
        print("[HINT] Install telnet client first, e.g. Ubuntu: sudo apt install telnet")
        return 5

    parser = argparse.ArgumentParser(description="Backup switch configs via Telnet")
    parser.add_argument(
        "--swinfo",
        default="swinfo.txt",
        help="Path to switch info file (default: swinfo.txt)",
    )
    parser.add_argument(
        "--out-dir",
        default=".",
        help="Output directory for backup files (default: current directory)",
    )
    parser.add_argument(
        "--default-password",
        default=os.environ.get("SWITCH_PASSWORD", ""),
        help="Fallback password when one is not present in swinfo line",
    )
    parser.add_argument("--timeout", type=int, default=15, help="Telnet connect timeout seconds")
    args = parser.parse_args()

    swinfo_path = Path(args.swinfo).resolve()
    out_dir = Path(args.out_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    # Create one folder per run: YYYYMMDD_HHMMSS
    run_folder = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
    run_out_dir = out_dir / run_folder
    run_out_dir.mkdir(parents=True, exist_ok=True)

    if not swinfo_path.exists():
        print(f"[ERROR] swinfo file not found: {swinfo_path}")
        return 2

    switches = parse_swinfo(swinfo_path, default_password=args.default_password)
    if not switches:
        print("[ERROR] No valid #telnet switches found to process")
        return 3

    print(f"[INFO] Loaded {len(switches)} switch(es) from {swinfo_path}")
    print(f"[INFO] Output folder: {run_out_dir}")

    ok_count = 0
    for sw in switches:
        print(f"[INFO] Backing up: {sw.position}/{sw.model}/{sw.ip}")
        ok, path, msg, elapsed = backup_one(sw, out_dir=run_out_dir, timeout=args.timeout)
        if ok:
            ok_count += 1
            print(f"[OK] {path}")
        else:
            print(f"[FAIL] {path} ({msg})")
        print(f"[INFO] Time used: {elapsed:.2f}s")

    print(f"[INFO] Done. success={ok_count}, failed={len(switches) - ok_count}")
    return 0 if ok_count == len(switches) else 1


if __name__ == "__main__":
    sys.exit(main())
