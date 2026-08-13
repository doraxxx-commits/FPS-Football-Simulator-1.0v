from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from urllib.parse import urlparse
import json,sys,os
sys.path.insert(0,os.path.dirname(__file__))
from demo_world import build_demo_world
from football_engine.game import CareerGame
game=CareerGame(build_demo_world())
class Handler(SimpleHTTPRequestHandler):
 def send_json(self,obj,status=200):
  data=json.dumps(obj,ensure_ascii=False,default=str).encode(); self.send_response(status); self.send_header("Content-Type","application/json; charset=utf-8"); self.send_header("Content-Length",str(len(data))); self.end_headers(); self.wfile.write(data)
 def do_GET(self):
  p=urlparse(self.path).path
  if p=="/api/state": return self.send_json(game.snapshot())
  if p=="/api/health": return self.send_json({"ok":True,"version":"6.0.0"})
  return super().do_GET()
 def do_POST(self):
  p=urlparse(self.path).path
  if p=="/api/season": game.play_season(); return self.send_json(game.snapshot())
  if p=="/api/save": game.save("career_save.json"); return self.send_json({"ok":True})
  self.send_json({"error":"not found"},404)
if __name__ == "__main__":
    # Render provides the public port through the PORT environment variable.
    # 8080 remains the local-development default.
    host = "0.0.0.0"
    port = int(os.environ.get("PORT", "8080"))
    print(f"Server listening on {host}:{port}")
    ThreadingHTTPServer((host, port), Handler).serve_forever()
