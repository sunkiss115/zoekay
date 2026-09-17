from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse
import json
import os
import threading
import time

ROOT = Path(__file__).resolve().parent
HOST = "127.0.0.1"
PORT = 8000
WATCHED_EXTENSIONS = {".html", ".css", ".js"}


def snapshot_files():
    return {
        str(path.relative_to(ROOT)): path.stat().st_mtime_ns
        for path in ROOT.rglob("*")
        if path.is_file()
        and ".git" not in path.parts
        and path.suffix.lower() in WATCHED_EXTENSIONS
    }


class LiveReloadState:
    def __init__(self):
        self.version = time.time_ns()
        self.clients = []
        self.lock = threading.Lock()

    def changed(self):
        with self.lock:
            self.version = time.time_ns()
            clients = list(self.clients)
            self.clients.clear()
        for client in clients:
            client.set()

    def wait_for_change(self, version):
        event = threading.Event()
        with self.lock:
            if self.version != version:
                return self.version
            self.clients.append(event)
        event.wait(timeout=30)
        return self.version


reload_state = LiveReloadState()


def watch_files():
    previous = snapshot_files()
    while True:
        time.sleep(0.5)
        current = snapshot_files()
        if current != previous:
            previous = current
            reload_state.changed()


class DevHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def do_GET(self):
        path = urlparse(self.path).path
        if path == "/__live_reload":
            self.send_live_reload()
            return
        if path == "/__live_reload.js":
            self.send_live_reload_script()
            return
        if path.endswith(".html") or path == "/":
            self.send_html(path)
            return
        super().do_GET()

    def send_html(self, path):
        file_path = ROOT / ("index.html" if path == "/" else path.lstrip("/"))
        if not file_path.is_file():
            self.send_error(404, "File not found")
            return
        content = file_path.read_bytes()
        marker = b"</body>"
        injection = b'<script src="/__live_reload.js"></script>'
        content = content.replace(marker, injection + marker, 1)
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def send_live_reload(self):
        try:
            version = int(self.headers.get("Last-Event-ID", reload_state.version))
        except ValueError:
            version = reload_state.version
        next_version = reload_state.wait_for_change(version)
        payload = json.dumps({"version": next_version}).encode()
        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream")
        self.send_header("Cache-Control", "no-cache")
        self.send_header("Connection", "keep-alive")
        self.send_header("Content-Length", str(len(payload) + 2))
        self.end_headers()
        self.wfile.write(b"data: " + payload + b"\n\n")

    def send_live_reload_script(self):
        script = """(() => {
  const connect = () => {
    const source = new EventSource('/__live_reload');
    source.onmessage = () => window.location.reload();
    source.onerror = () => { source.close(); setTimeout(connect, 1000); };
  };
  connect();
})();
"""
        body = script.encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/javascript; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_HEAD(self):
        super().do_HEAD()


if __name__ == "__main__":
    threading.Thread(target=watch_files, daemon=True).start()
    server = ThreadingHTTPServer((HOST, PORT), DevHandler)
    print(f"Serving {ROOT}")
    print(f"Open http://{HOST}:{PORT}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped")
        server.server_close()
