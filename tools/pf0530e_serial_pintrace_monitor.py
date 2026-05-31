#!/usr/bin/env python3
"""Read-only COM transcript helper for the PF0530E serial pintrace image."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path
import sys
import time


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Monitor PF0530E serial pintrace output without sending bytes."
    )
    parser.add_argument("--port", default="COM6", help="Windows COM port.")
    parser.add_argument("--baud", type=int, default=115200, help="Serial baud.")
    parser.add_argument("--out", required=True, help="Transcript output path.")
    parser.add_argument(
        "--duration",
        type=float,
        default=0.0,
        help="Seconds to monitor; 0 means run until interrupted.",
    )
    return parser.parse_args()


def utc_stamp() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds")


def main() -> int:
    args = parse_args()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(errors="backslashreplace")
    try:
        import serial
    except ImportError as exc:
        print(f"pyserial unavailable: {exc}", file=sys.stderr)
        return 2

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    deadline = None if args.duration <= 0 else time.monotonic() + args.duration

    with serial.Serial(args.port, args.baud, timeout=0.2) as handle:
        with out_path.open("a", encoding="utf-8", newline="\n") as transcript:
            header = (
                f"# PF0530E serial pintrace monitor start={utc_stamp()} "
                f"port={args.port} baud={args.baud} writes_sent=false\n"
            )
            transcript.write(header)
            transcript.flush()
            sys.stdout.write(header)
            sys.stdout.flush()

            try:
                while deadline is None or time.monotonic() < deadline:
                    data = handle.readline()
                    if not data:
                        continue
                    text = data.decode("utf-8", errors="replace").rstrip("\r\n")
                    line = f"{utc_stamp()} {text}\n"
                    transcript.write(line)
                    transcript.flush()
                    sys.stdout.write(line)
                    sys.stdout.flush()
            except KeyboardInterrupt:
                pass

            footer = f"# PF0530E serial pintrace monitor stop={utc_stamp()}\n"
            transcript.write(footer)
            transcript.flush()
            sys.stdout.write(footer)
            sys.stdout.flush()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
