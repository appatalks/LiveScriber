#!/usr/bin/env python3
"""Generate LiveScribe Pro license keys.

Usage:
    python scripts/generate_license.py            # generate one key
    python scripts/generate_license.py 5           # generate five keys
    python scripts/generate_license.py --verify XXXX-XXXX-XXXX-XXXX

Keys use the format XXXX-XXXX-XXXX-XXXX.
The first three groups are random alphanumeric, and the fourth is a
SHA-256 checksum of the first three, so the app can validate offline
without a license server.
"""

from __future__ import annotations

import hashlib
import secrets
import string
import sys


CHARSET = string.ascii_uppercase + string.digits


def _random_group() -> str:
    return "".join(secrets.choice(CHARSET) for _ in range(4))


def generate_key() -> str:
    groups = [_random_group() for _ in range(3)]
    payload = "-".join(groups)
    checksum = hashlib.sha256(
        ("LiveScribePro:" + payload).encode()
    ).hexdigest()[:4].upper()
    return f"{payload}-{checksum}"


def validate_key(key: str) -> bool:
    parts = key.strip().upper().split("-")
    if len(parts) != 4 or not all(len(p) == 4 and p.isalnum() for p in parts):
        return False
    payload = "-".join(parts[:3])
    expected = hashlib.sha256(
        ("LiveScribePro:" + payload).encode()
    ).hexdigest()[:4].upper()
    return parts[3] == expected


def main():
    if len(sys.argv) >= 3 and sys.argv[1] == "--verify":
        key = sys.argv[2]
        valid = validate_key(key)
        print(f"{key}  {'✓ valid' if valid else '✗ invalid'}")
        raise SystemExit(0 if valid else 1)

    count = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    for _ in range(count):
        print(generate_key())


if __name__ == "__main__":
    main()
