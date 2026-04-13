import argparse
import subprocess
import re
import random
import time
import ipaddress


def run_nslookup(domain):
    result = subprocess.run(
        ["nslookup", domain],
        capture_output=True, text=True, timeout=30
    )
    return result.stdout + result.stderr


def parse_ips(output, domain):
    ipv4s = set()
    ipv6s = set()
    lines = output.splitlines()
    # Skip the first "Name Server" section, parse only the answer section
    in_answer = False
    for line in lines:
        stripped = line.strip()
        if domain.lower() in stripped.lower():
            in_answer = True
            continue
        if in_answer:
            # Match IPv4 addresses
            v4_matches = re.findall(r'\b(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\b', stripped)
            for addr in v4_matches:
                try:
                    ipaddress.IPv4Address(addr)
                    ipv4s.add(addr)
                except ValueError:
                    pass
            # Match IPv6 addresses (lines starting with "Address:" or containing ::)
            v6_matches = re.findall(r'(?i)(?:address[es]*:\s*)?([0-9a-f:]{3,}(?:::[0-9a-f:]*|(?::[0-9a-f]{1,4}){5,}))', stripped)
            for addr in v6_matches:
                try:
                    ipaddress.IPv6Address(addr)
                    ipv6s.add(addr)
                except ValueError:
                    pass
    return ipv4s, ipv6s


def save_results(domain, ipv4s, ipv6s):
    filename = f"dns_{domain}.txt"
    sorted_v4 = sorted(ipv4s, key=lambda x: ipaddress.IPv4Address(x))
    sorted_v6 = sorted(ipv6s, key=lambda x: ipaddress.IPv6Address(x))
    with open(filename, "w", encoding="utf-8") as f:
        if sorted_v4:
            f.write("IPv4 Addresses:\n")
            for addr in sorted_v4:
                f.write(f"{addr}\n")
        if sorted_v4 and sorted_v6:
            f.write("\n")
        if sorted_v6:
            f.write("IPv6 Addresses:\n")
            for addr in sorted_v6:
                f.write(f"{addr}\n")
    return filename


def main():
    parser = argparse.ArgumentParser(description="DNS lookup and collect all resolved IPs")
    parser.add_argument("-n", required=True, help="Domain name to query")
    args = parser.parse_args()
    domain = args.n

    all_v4 = set()
    all_v6 = set()
    total_runs = 10

    for i in range(1, total_runs + 1):
        print(f"[{i}/{total_runs}] Running nslookup {domain} ...")
        try:
            output = run_nslookup(domain)
            v4, v6 = parse_ips(output, domain)
            all_v4.update(v4)
            all_v6.update(v6)
            print(f"  Found IPv4: {len(v4)}, IPv6: {len(v6)}  |  Total so far: IPv4={len(all_v4)}, IPv6={len(all_v6)}")
        except Exception as e:
            print(f"  Error: {e}")

        if i < total_runs:
            wait = random.uniform(20, 30)
            print(f"  Waiting {wait:.1f}s ...")
            time.sleep(wait)

    filename = save_results(domain, all_v4, all_v6)
    total = len(all_v4) + len(all_v6)
    print(f"\nDone. 总共发现的IP地址数量: {total} (IPv4: {len(all_v4)}, IPv6: {len(all_v6)})")
    print(f"Results saved to {filename}")


if __name__ == "__main__":
    main()
