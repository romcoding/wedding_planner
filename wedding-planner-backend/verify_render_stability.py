#!/usr/bin/env python3
"""Lightweight post-deploy verification for Render stability."""

from __future__ import annotations

import argparse
import csv
import sys
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Iterable
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


DEFAULT_ENDPOINTS = (
    "/api/health",
    "/api/content?lang=en",
    "/api/images",
    "/api/events/guest-portal-settings",
)


@dataclass
class CheckResult:
    timestamp: str
    endpoint: str
    status_code: int
    latency_ms: int
    response_bytes: int
    ok: bool
    error: str


def check_endpoint(base_url: str, endpoint: str, timeout: int) -> CheckResult:
    url = f"{base_url.rstrip('/')}{endpoint}"
    started = time.perf_counter()
    now = datetime.now(timezone.utc).isoformat()

    request = Request(url, headers={"User-Agent": "render-stability-check/1.0"})

    try:
        with urlopen(request, timeout=timeout) as response:
            payload = response.read()
            latency_ms = int((time.perf_counter() - started) * 1000)
            status_code = int(response.status)
            ok = 200 <= status_code < 400
            return CheckResult(
                timestamp=now,
                endpoint=endpoint,
                status_code=status_code,
                latency_ms=latency_ms,
                response_bytes=len(payload),
                ok=ok,
                error="",
            )
    except HTTPError as exc:
        latency_ms = int((time.perf_counter() - started) * 1000)
        return CheckResult(
            timestamp=now,
            endpoint=endpoint,
            status_code=exc.code,
            latency_ms=latency_ms,
            response_bytes=0,
            ok=False,
            error=f"HTTPError: {exc.reason}",
        )
    except URLError as exc:
        latency_ms = int((time.perf_counter() - started) * 1000)
        return CheckResult(
            timestamp=now,
            endpoint=endpoint,
            status_code=0,
            latency_ms=latency_ms,
            response_bytes=0,
            ok=False,
            error=f"URLError: {exc.reason}",
        )


def run_checks(base_url: str, endpoints: Iterable[str], timeout: int) -> list[CheckResult]:
    return [check_endpoint(base_url, endpoint, timeout) for endpoint in endpoints]


def print_results(results: list[CheckResult]) -> None:
    print("timestamp,endpoint,status,latency_ms,response_bytes,ok,error")
    for result in results:
        print(
            f"{result.timestamp},{result.endpoint},{result.status_code},"
            f"{result.latency_ms},{result.response_bytes},{result.ok},{result.error}"
        )


def append_csv(csv_path: str, results: list[CheckResult]) -> None:
    with open(csv_path, "a", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        for result in results:
            writer.writerow(
                [
                    result.timestamp,
                    result.endpoint,
                    result.status_code,
                    result.latency_ms,
                    result.response_bytes,
                    result.ok,
                    result.error,
                ]
            )


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify backend endpoint stability after deploy.")
    parser.add_argument("--base-url", required=True, help="Base backend URL, e.g. https://api.example.com")
    parser.add_argument("--timeout", type=int, default=15, help="Per-request timeout in seconds")
    parser.add_argument("--interval-seconds", type=int, default=300, help="Polling interval for monitoring mode")
    parser.add_argument("--duration-hours", type=float, default=0, help="If > 0, monitor continuously for this duration")
    parser.add_argument("--csv", default="render_stability_checks.csv", help="CSV output file path")
    parser.add_argument("--include-admin-endpoint", action="store_true", help="Include /api/events/guest-portal-settings")
    args = parser.parse_args()

    endpoints = list(DEFAULT_ENDPOINTS)
    if not args.include_admin_endpoint:
        endpoints.remove("/api/events/guest-portal-settings")

    if args.duration_hours <= 0:
        results = run_checks(args.base_url, endpoints, args.timeout)
        print_results(results)
        append_csv(args.csv, results)
        return 0 if all(item.ok for item in results) else 1

    deadline = time.time() + int(args.duration_hours * 3600)
    overall_ok = True
    while time.time() <= deadline:
        results = run_checks(args.base_url, endpoints, args.timeout)
        print_results(results)
        append_csv(args.csv, results)
        if not all(item.ok for item in results):
            overall_ok = False
        time.sleep(args.interval_seconds)

    return 0 if overall_ok else 1


if __name__ == "__main__":
    sys.exit(main())
