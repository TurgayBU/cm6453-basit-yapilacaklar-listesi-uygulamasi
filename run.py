"""Üretilen uygulamayı başlatır: backend'i çalıştırır, arayüzü tarayıcıda açar.

    python3 run.py

Kapatmak için Ctrl+C. CM6453 Agent Platform tarafından üretildi.
"""
import socket
import subprocess
import sys
import time
import webbrowser
from pathlib import Path

HERE = Path(__file__).resolve().parent
BACKEND = HERE / "backend" / "app.py"
FRONTEND = HERE / "frontend" / "index.html"
PORT = 9000  # Backend Agent'ın varsayılan portu; arayüz API_BASE ile buna bağlanır


def wait_for_port(port, timeout=15.0):
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            with socket.create_connection(("127.0.0.1", port), timeout=0.5):
                return True
        except OSError:
            time.sleep(0.3)
    return False


def main():
    if not BACKEND.exists():
        sys.exit("backend/app.py yok: bu yapımda backend üretilmemiş.")
    server = subprocess.Popen([sys.executable, BACKEND.name], cwd=BACKEND.parent)
    try:
        if not wait_for_port(PORT):
            sys.exit(f"Backend {PORT} portunda açılmadı; çıktıyı yukarıda kontrol edin.")
        print(f"Backend çalışıyor: http://localhost:{PORT}")
        if FRONTEND.exists():
            webbrowser.open(FRONTEND.as_uri())
            print(f"Arayüz açıldı: {FRONTEND}")
        print("Kapatmak için Ctrl+C")
        server.wait()
    except KeyboardInterrupt:
        pass
    finally:
        server.terminate()


if __name__ == "__main__":
    main()
