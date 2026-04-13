#!/usr/bin/env python3
"""
Backup switch output over SSH.

Requirements:
- Python package: pexpect
- System ssh client available in PATH

Input file format (sshsw.txt):
    name,ip,username,password[,enable_password]

For each switch, the script:
1) SSH login
2) runs: show version
3) runs: exit
4) saves terminal output to local file

Output:
- Creates one run directory: YYYYMMDD_HHMMSS
- File naming: {name}_{ip}_{YYYYMMDD_HHMMSS}.txt
"""

from __future__ import annotations

import argparse
import datetime as dt
import importlib
import re
import shutil
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, List, Optional, Tuple

try:
    pexpect = importlib.import_module("pexpect")
except ModuleNotFoundError:
    pexpect = None

PROMPT_PATTERN = r"(?m)[\r\n].{0,120}[>#]\s?$"
PRIV_PROMPT_PATTERN = r"(?m)[\r\n].{0,120}#\s?$"
MORE_PATTERNS = [r"--More--", r"---- More ----", r"<--- More --->", r"\[More\]"]
COLLECT_COMMANDS = [
    "show version",
    "show vlan",
    "show inter desc",
    "show interfaces status",
    "show run",
]


@dataclass
class SSHSwitch:
    name: str
    ip: str
    username: str
    password: str
    enable_password: str = ""


def detect_switch_type(name: str) -> str:
    n = name.lower()
    if "1300" in n:
        return "cisco1300"
    if "9200" in n:
        return "cisco9200"
    return "common"


def sanitize_name(name: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", name).strip("_") or "switch"


def sanitize_output_text(text: str) -> str:
    """Remove terminal control artifacts from captured transcript text."""
    if not text:
        return text

    # Normalize line endings first.
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    # Resolve backspace-overstrike patterns repeatedly (e.g. 'X\b').
    prev = None
    while prev != text:
        prev = text
        text = re.sub(r"[^\n]\x08", "", text)

    # Drop remaining raw backspaces and other C0 controls (except \n and \t).
    text = text.replace("\x08", "")
    text = re.sub(r"[\x00-\x09\x0b-\x1f\x7f]", "", text)

    # If caret notation leaked into files, remove these markers too.
    text = text.replace("^H", "").replace("^M", "")

    return text


def parse_sshsw(path: Path) -> List[SSHSwitch]:
    switches: List[SSHSwitch] = []
    with path.open("r", encoding="utf-8") as f:
        for raw in f:
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            parts = [p.strip() for p in line.split(",")]
            if len(parts) < 4:
                print(f"[WARN] Skip invalid line: {line}")
                continue
            name, ip, username, password = parts[0], parts[1], parts[2], parts[3]
            enable_password = parts[4] if len(parts) >= 5 else ""
            if not (name and ip and username and password):
                print(f"[WARN] Skip incomplete line: {line}")
                continue
            switches.append(
                SSHSwitch(
                    name=name,
                    ip=ip,
                    username=username,
                    password=password,
                    enable_password=enable_password,
                )
            )
    return switches


def read_until_any(child: Any, patterns: List[str], timeout: float) -> Tuple[str, Optional[str]]:
    if pexpect is None:
        return "", None
    try:
        idx = child.expect(patterns + [pexpect.TIMEOUT, pexpect.EOF], timeout=timeout)
    except Exception:
        return "", None

    data = child.before or ""
    if isinstance(child.after, str):
        data += child.after

    if idx < len(patterns):
        return data, patterns[idx]
    if idx == len(patterns) + 1:
        data += "\n[connection-closed-by-remote]\n"
    return data, None


def read_command_output(child: Any, timeout: float) -> str:
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
                # Advance paged output.
                child.send(" ")
                data += "\n[auto-send-space-for-more]\n"
                continue
            if idx == len(MORE_PATTERNS):
                break
            if idx == len(MORE_PATTERNS) + 1:
                continue
            if idx == len(MORE_PATTERNS) + 2:
                data += "\n[connection-closed-by-remote]\n"
                break
        except Exception as exc:
            data += f"\n[read-error] {type(exc).__name__}: {exc}\n"
            break

    return data


def wait_for_prompt(child: Any, timeout: float) -> Tuple[bool, str]:
    """Wait until a normal device prompt is reached."""
    if pexpect is None:
        return False, ""
    end = time.time() + timeout
    data = ""
    while time.time() < end:
        idx = child.expect([PROMPT_PATTERN, r"(?i)password[: ]*$", pexpect.TIMEOUT, pexpect.EOF], timeout=1.0)
        part = child.before or ""
        if isinstance(child.after, str):
            part += child.after
        data += part
        if idx == 0:
            return True, data
        if idx == 1:
            # Password prompt here usually means login not complete.
            return False, data + "\n[unexpected-password-prompt]\n"
        if idx == 3:
            return False, data + "\n[connection-closed-by-remote]\n"
    return False, data + "\n[prompt-timeout]\n"


def wait_for_privileged_prompt(child: Any, timeout: float) -> Tuple[bool, str]:
    """Wait until privileged prompt (#) is reached."""
    if pexpect is None:
        return False, ""
    end = time.time() + timeout
    data = ""
    user_prompt = r"(?m)[\r\n].{0,120}>\s?$"
    while time.time() < end:
        idx = child.expect(
            [PRIV_PROMPT_PATTERN, user_prompt, r"(?i)password[: ]*$", pexpect.TIMEOUT, pexpect.EOF],
            timeout=1.0,
        )
        part = child.before or ""
        if isinstance(child.after, str):
            part += child.after
        data += part
        if idx == 0:
            return True, data
        if idx == 1:
            # still at user mode prompt, keep waiting
            continue
        if idx == 2:
            # got password challenge again, caller may need to resend password
            return False, data + "\n[unexpected-password-prompt]\n"
        if idx == 4:
            return False, data + "\n[connection-closed-by-remote]\n"
    return False, data + "\n[priv-prompt-timeout]\n"


def backup_one(sw: SSHSwitch, out_dir: Path, connect_timeout: int) -> Tuple[bool, Path, str, float]:
    start = time.perf_counter()
    ts = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_name = sanitize_name(sw.name)
    out_file = out_dir / f"{safe_name}_{sw.ip}_{ts}.txt"

    transcript: List[str] = []
    transcript.append(f"=== Backup Start: {dt.datetime.now().isoformat()} ===")
    sw_type = detect_switch_type(sw.name)
    transcript.append(f"name={sw.name}, ip={sw.ip}, username={sw.username}, type={sw_type}")

    try:
        base = (
            f"ssh -o StrictHostKeyChecking=no "
            f"-o UserKnownHostsFile=/dev/null "
            f"-o ConnectTimeout={connect_timeout} "
        )
        # cisco1300 requires `ssh ip` then interactive "User Name" prompt.
        if sw_type == "cisco1300":
            cmd = base + f"{sw.ip}"
        else:
            cmd = base + f"{sw.username}@{sw.ip}"
        child = pexpect.spawn(cmd, encoding="utf-8", codec_errors="replace", timeout=connect_timeout)

        # Unified login state machine for all types.
        # Handles: host-key confirm, User Name/Username, Password, auth failure, prompt.
        logged_in = False
        pw_tries = 0
        for phase in range(1, 16):
            idx = child.expect(
                [
                    r"(?i)are you sure you want to continue connecting",
                    r"(?i)user\s*name\s*:",
                    r"(?i)username\s*:",
                    r"(?i)password\s*:",
                    r"(?i)permission denied|authentication failed|access denied|login invalid",
                    PROMPT_PATTERN,
                    pexpect.TIMEOUT,
                    pexpect.EOF,
                ],
                timeout=max(6.0, float(connect_timeout)),
            )

            phase_data = (child.before or "")
            if isinstance(child.after, str):
                phase_data += child.after
            if phase_data:
                transcript.append(f"\n--- Login Phase {phase} ---\n" + phase_data)

            if idx == 0:
                child.sendline("yes")
                continue

            if idx in (1, 2):
                child.sendline(sw.username)
                continue

            if idx == 3:
                pw_tries += 1
                child.sendline(sw.password)
                if pw_tries >= 3:
                    raise RuntimeError(f"{sw_type} login failed: password rejected")
                continue

            if idx == 4:
                raise RuntimeError(f"{sw_type} login failed: authentication denied")

            if idx == 5:
                logged_in = True
                break

            if idx == 6:
                # timeout slice, keep waiting for next login challenge or prompt
                continue

            if idx == 7:
                raise RuntimeError(f"{sw_type} login failed: connection closed")

        if not logged_in:
            raise RuntimeError(f"{sw_type} login failed: prompt not reached")

        post_login = read_command_output(child, timeout=3.0)
        if post_login:
            transcript.append("\n--- Post Login ---\n" + post_login)

        # cisco9200 needs enable mode before show commands.
        if sw_type == "cisco9200":
            enable_password = sw.enable_password or sw.password
            child.sendline("enable")
            enable_data, enable_matched = read_until_any(
                child,
                [r"(?i)password[: ]*$", PROMPT_PATTERN],
                timeout=6.0,
            )
            transcript.append("\n$ enable\n" + (enable_data or ""))
            enable_ok = bool(enable_data and re.search(PRIV_PROMPT_PATTERN, enable_data))
            if enable_matched and re.search(r"password", enable_matched, flags=re.IGNORECASE):
                child.sendline(enable_password)
                enable_done = read_command_output(child, timeout=6.0)
                transcript.append(enable_done)
                if re.search(PRIV_PROMPT_PATTERN, enable_done):
                    enable_ok = True

            # Safety guard: must be in privileged mode (#) before show commands.
            if enable_ok:
                ok_priv, priv_data = True, "[privileged-prompt-already-captured]"
            else:
                ok_priv, priv_data = wait_for_privileged_prompt(child, timeout=8.0)
            if priv_data:
                transcript.append("\n--- Privileged Prompt Check ---\n" + priv_data)
            if not ok_priv:
                raise RuntimeError("cisco9200 enable failed: privileged prompt (#) not reached")

        # Required command set
        for cmd in COLLECT_COMMANDS:
            child.sendline(cmd)
            cmd_timeout = 120.0 if cmd == "show run" else 40.0
            cmd_out = read_command_output(child, timeout=cmd_timeout)
            transcript.append(f"\n$ {cmd}\n" + cmd_out)

        # Required exit
        child.sendline("exit")
        exit_out = read_command_output(child, timeout=5.0)
        transcript.append("\n$ exit\n" + exit_out)

        try:
            child.close(force=True)
        except Exception:
            pass

        elapsed = time.perf_counter() - start
        transcript.append(f"elapsed_seconds={elapsed:.2f}")
        transcript.append(f"=== Backup End: {dt.datetime.now().isoformat()} ===")

        out_file.write_text(sanitize_output_text("\n".join(transcript)), encoding="utf-8", errors="replace")
        return True, out_file, "ok", elapsed

    except Exception as exc:
        elapsed = time.perf_counter() - start
        transcript.append(f"[ERROR] {type(exc).__name__}: {exc}")
        transcript.append(f"elapsed_seconds={elapsed:.2f}")
        transcript.append(f"=== Backup End (Failed): {dt.datetime.now().isoformat()} ===")
        out_file.write_text(sanitize_output_text("\n".join(transcript)), encoding="utf-8", errors="replace")
        return False, out_file, str(exc), elapsed


def main() -> int:
    if pexpect is None:
        print("[ERROR] Missing dependency: pexpect")
        print("[HINT] Install with: pip install pexpect")
        return 4

    if shutil.which("ssh") is None:
        print("[ERROR] 'ssh' command not found in PATH")
        return 5

    parser = argparse.ArgumentParser(description="Backup switches via SSH and save 'show version' output")
    parser.add_argument("--swinfo", default="sshsw.txt", help="Path to ssh switch info file")
    parser.add_argument("--out-dir", default=".", help="Output base directory")
    parser.add_argument("--timeout", type=int, default=15, help="SSH connect timeout seconds")
    args = parser.parse_args()

    swinfo_path = Path(args.swinfo).resolve()
    out_dir = Path(args.out_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    if not swinfo_path.exists():
        print(f"[ERROR] swinfo file not found: {swinfo_path}")
        return 2

    switches = parse_sshsw(swinfo_path)
    if not switches:
        print("[ERROR] No valid switch entries found")
        return 3

    run_folder = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
    run_out_dir = out_dir / run_folder
    run_out_dir.mkdir(parents=True, exist_ok=True)

    print(f"[INFO] Loaded {len(switches)} switch(es)")
    print(f"[INFO] Output folder: {run_out_dir}")

    ok = 0
    for sw in switches:
        print(f"[INFO] Backing up: {sw.name}/{sw.ip}")
        success, path, msg, elapsed = backup_one(sw, run_out_dir, connect_timeout=args.timeout)
        if success:
            ok += 1
            print(f"[OK] {path}")
        else:
            print(f"[FAIL] {path} ({msg})")
        print(f"[INFO] Time used: {elapsed:.2f}s")

    print(f"[INFO] Done. success={ok}, failed={len(switches) - ok}")
    return 0 if ok == len(switches) else 1


if __name__ == "__main__":
    sys.exit(main())
