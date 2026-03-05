#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import socket
import subprocess
import time
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def check_network():
    sites = ['github.com', 'gumroad.com', 'pypi.org']
    for site in sites:
        try:
            socket.create_connection((site, 80), timeout=3)
            print(f"[OK] {site}")
        except Exception as e:
            print(f"[X] {site}: {e}")

if __name__ == "__main__":
    print("=== Jarvis Daily Check ===")
    print("Network:")
    check_network()
    print("\n=== Quick Actions ===")
    print("1. Check Gumroad sales")
    print("2. GitHub Stars -> Sponsors")
    print("3. Create paid product")
    print("4. Write tech blog")
    print("5. Upwork/Fiverr gigs")
