import http.server
import socketserver
import sys
import os
import subprocess
import time

os.chdir(os.path.dirname(os.path.abspath(__file__)))

class NoCacheHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()

PORT = 8080
socketserver.TCPServer.allow_reuse_address = True

def free_port(port):
    try:
        cmd = 'netstat -ano'
        out = subprocess.check_output(cmd, shell=True).decode('utf-8', errors='ignore')
        my_pid = str(os.getpid())
        for line in out.splitlines():
            if f':{port} ' in line:
                tokens = line.strip().split()
                if len(tokens) >= 5:
                    pid = tokens[-1]
                    if pid != '0' and pid != my_pid:
                        subprocess.run(f'taskkill /F /PID {pid}', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(0.5)
    except Exception:
        pass

if __name__ == '__main__':
    httpd = None
    for attempt in range(3):
        try:
            httpd = socketserver.TCPServer(('127.0.0.1', PORT), NoCacheHandler)
            break
        except OSError:
            print(f"Port {PORT} belegt. Bereinige vorherigen Prozess...")
            free_port(PORT)
            time.sleep(0.5)

    if not httpd:
        print(f"Fehler: Konnte Port {PORT} nicht binden.")
        sys.exit(1)

    print(f"Server gestartet auf http://127.0.0.1:{PORT}")
    print("Druecken Sie Strg+C zum Beenden.")
    sys.stdout.flush()
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer wird beendet...")
        httpd.server_close()
