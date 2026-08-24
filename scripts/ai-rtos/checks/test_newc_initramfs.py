#!/usr/bin/env python3
# Copyright 2026 The TGOSKits Authors
#
# SPDX-License-Identifier: Apache-2.0

"""Regression coverage for the portable newc initramfs fallback."""

from __future__ import annotations

import pathlib
import subprocess
import sys
import tempfile


def align(value: int) -> int:
    return (value + 3) & ~3


def read_entries(archive: bytes) -> dict[str, int]:
    offset = 0
    entries: dict[str, int] = {}
    while True:
        header = archive[offset : offset + 110]
        if len(header) != 110 or header[:6] != b"070701":
            raise AssertionError(f"invalid newc header at offset {offset}")
        values = [int(header[index : index + 8], 16) for index in range(6, 110, 8)]
        mode, payload_size, name_size = values[1], values[6], values[11]
        offset += 110
        name = archive[offset : offset + name_size - 1].decode()
        offset = align(offset + name_size)
        offset = align(offset + payload_size)
        if name == "TRAILER!!!":
            return entries
        entries[name] = mode


def main() -> None:
    repo_root = pathlib.Path(__file__).resolve().parents[3]
    writer = repo_root / "scripts/ai-rtos/lib/newc_initramfs.py"
    with tempfile.TemporaryDirectory(prefix="aicp-newc-") as temporary:
        root = pathlib.Path(temporary)
        init = root / "init"
        init.write_text("#!/bin/sh\necho ready\n")
        init.chmod(0o755)
        (root / "lib").mkdir()
        (root / "lib" / "runtime.so").write_bytes(b"runtime")
        archive = subprocess.run(
            [sys.executable, str(writer), str(root)],
            check=True,
            stdout=subprocess.PIPE,
        ).stdout

    entries = read_entries(archive)
    expected = {".", "init", "lib", "lib/runtime.so"}
    if set(entries) != expected:
        raise AssertionError(f"unexpected archive entries: {sorted(entries)}")
    if entries["init"] & 0o111 == 0:
        raise AssertionError("init executable mode was not preserved")
    print("PASS: portable newc initramfs writer")


if __name__ == "__main__":
    main()
