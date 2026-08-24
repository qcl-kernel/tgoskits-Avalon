#!/usr/bin/env python3
# Copyright 2026 The TGOSKits Authors
#
# SPDX-License-Identifier: Apache-2.0

"""Write a reproducible Linux ``newc`` initramfs from one directory.

This is a narrow fallback for hosts where the standard ``cpio`` executable is
unavailable. It supports the file kinds produced by the AICP initramfs staging
directory: directories, regular files and symbolic links.
"""

from __future__ import annotations

import os
import pathlib
import stat
import sys


NEWC_MAGIC = b"070701"
TRAILER = "TRAILER!!!"


def align(value: int) -> int:
    return (value + 3) & ~3


def write_padding(output: object, size: int) -> None:
    padding = align(size) - size
    if padding:
        output.write(b"\0" * padding)


def entry_payload(path: pathlib.Path, file_mode: int) -> bytes:
    if stat.S_ISREG(file_mode):
        return path.read_bytes()
    if stat.S_ISLNK(file_mode):
        return os.fsencode(os.readlink(path))
    return b""


def write_entry(output: object, name: str, path: pathlib.Path | None) -> None:
    if path is None:
        file_mode = stat.S_IFREG
        uid = gid = mtime = 0
        nlink = 1
        payload = b""
    else:
        metadata = path.lstat()
        file_mode = metadata.st_mode
        if not (stat.S_ISDIR(file_mode) or stat.S_ISREG(file_mode) or stat.S_ISLNK(file_mode)):
            raise ValueError(f"unsupported initramfs entry type: {path}")
        uid = metadata.st_uid
        gid = metadata.st_gid
        mtime = int(metadata.st_mtime)
        nlink = metadata.st_nlink
        payload = entry_payload(path, file_mode)

    encoded_name = os.fsencode(name) + b"\0"
    header_fields = (
        0,
        file_mode,
        uid,
        gid,
        nlink,
        mtime,
        len(payload),
        0,
        0,
        0,
        0,
        len(encoded_name),
        0,
    )
    output.write(NEWC_MAGIC)
    output.write(b"".join(f"{field:08x}".encode() for field in header_fields))
    output.write(encoded_name)
    write_padding(output, 110 + len(encoded_name))
    output.write(payload)
    write_padding(output, len(payload))


def iter_entries(root: pathlib.Path) -> list[tuple[str, pathlib.Path]]:
    entries = [(".", root)]
    for current, directories, files in os.walk(root, followlinks=False):
        directories.sort()
        files.sort()
        parent = pathlib.Path(current)
        for child in directories + files:
            path = parent / child
            entries.append((path.relative_to(root).as_posix(), path))
    return entries


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit(f"usage: {pathlib.Path(sys.argv[0]).name} <staging-dir>")
    root = pathlib.Path(sys.argv[1])
    if not root.is_dir():
        raise SystemExit(f"initramfs staging directory does not exist: {root}")

    output = sys.stdout.buffer
    for name, path in iter_entries(root):
        write_entry(output, name, path)
    write_entry(output, TRAILER, None)


if __name__ == "__main__":
    main()
