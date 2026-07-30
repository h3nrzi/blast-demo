import os
import json
import subprocess
import sys
from http.server import HTTPServer, SimpleHTTPRequestHandler

PORT = 8080
PUBLIC_DIR = os.path.join(os.path.dirname(__file__), "public")
PAYLOAD_FILE = os.path.join(os.path.dirname(__file__), ".tmp", "processed_dashboard_payload.json")

class BLASTDashboardHandler(SimpleHTTPRequestHandler):
    def translate_path(self, path):
        # Serve static files from public directory
        clean_path = path.split('?', 1)[0].split('#', 1)[0]
        if clean_path in ["/", "/index.html"]:
            return os.path.join(PUBLIC_DIR, "index.html")
        elif clean_path == "/styles.css":
            return os.path.join(PUBLIC_DIR, "styles.css")
        elif clean_path == "/app.js":
            return os.path.join(PUBLIC_DIR, "app.js")
        return super().translate_path(path)

    def do_GET(self):
        clean_path = self.path.split('?', 1)[0]
        if clean_path == "/api/articles":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            
            if os.path.exists(PAYLOAD_FILE):
                with open(PAYLOAD_FILE, "rb") as f:
                    self.wfile.write(f.read())
            else:
                self.wfile.write(json.dumps({"articles": [], "metadata": {"total_count": 0}}).encode("utf-8"))
        else:
            super().do_GET()

    def do_POST(self):
        clean_path = self.path.split('?', 1)[0]
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length).decode('utf-8') if content_length > 0 else "{}"
        
        try:
            body = json.loads(post_data)
        except Exception:
            body = {}

        if clean_path == "/api/bookmark":
            article_id = body.get("article_id")
            if article_id:
                # Trigger tools/store_bookmarks.py
                cmd = [sys.executable, "tools/store_bookmarks.py", article_id]
                res = subprocess.run(cmd, capture_output=True, text=True)
                
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(res.stdout.encode("utf-8"))
            else:
                self.send_error(400, "Missing article_id")

        elif clean_path == "/api/refresh":
            print("[SERVER] Triggering main.py feed refresh...")
            res = subprocess.run([sys.executable, "main.py"], capture_output=True, text=True)
            
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            
            if res.returncode == 0:
                # Read updated count
                total_count = 0
                if os.path.exists(PAYLOAD_FILE):
                    with open(PAYLOAD_FILE, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        total_count = data.get("metadata", {}).get("total_count", 0)
                        
                self.wfile.write(json.dumps({"success": True, "total_count": total_count}).encode("utf-8"))
            else:
                self.wfile.write(json.dumps({"success": False, "error": res.stderr}).encode("utf-8"))

        else:
            self.send_error(404, "Endpoint not found")

def main():
    server_address = ('', PORT)
    httpd = HTTPServer(server_address, BLASTDashboardHandler)
    print(f"🚀 AI News Radar Dashboard Server running at http://localhost:{PORT}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping server...")
        httpd.server_close()

if __name__ == "__main__":
    main()
