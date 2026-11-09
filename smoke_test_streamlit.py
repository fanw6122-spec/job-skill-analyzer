"""Execute the real Streamlit script, then verify a local HTTP server boots."""

from __future__ import annotations

import socket
import subprocess
import sys
import time
from pathlib import Path
from urllib.error import URLError
from urllib.request import urlopen


ROOT = Path(__file__).resolve().parent


def _open_port() -> int:
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


def check_app_script() -> None:
    from streamlit.testing.v1 import AppTest

    app = AppTest.from_file(str(ROOT / "streamlit_app.py"), default_timeout=15).run()
    if len(app.exception):
        raise AssertionError(f"Streamlit script raised an exception: {app.exception}")
    print("[PASS] Real Streamlit script executes with no upload.")


def check_http_server() -> None:
    port = _open_port()
    command = [
        sys.executable,
        "-m", "streamlit", "run", str(ROOT / "streamlit_app.py"),
        "--server.headless=true",
        "--browser.gatherUsageStats=false",
        "--server.address=127.0.0.1",
        f"--server.port={port}",
    ]
    process = subprocess.Popen(command, cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        deadline = time.monotonic() + 30
        while time.monotonic() < deadline:
            if process.poll() is not None:
                raise AssertionError(f"Streamlit exited unexpectedly ({process.returncode})")
            try:
                with urlopen(f"http://127.0.0.1:{port}/_stcore/health", timeout=1) as response:
                    if response.status == 200:
                        print("[PASS] Local Streamlit HTTP health endpoint responds.")
                        return
            except (OSError, URLError):
                pass
            time.sleep(0.2)
        raise AssertionError("Streamlit did not become healthy within 30 seconds")
    finally:
        process.terminate()
        try:
            process.wait(timeout=10)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait(timeout=5)


def main() -> None:
    check_app_script()
    check_http_server()
    print("[PASS] Real Streamlit startup checks completed.")


if __name__ == "__main__":
    main()
