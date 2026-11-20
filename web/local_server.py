"""Run the web demo on your own computer, the same way Vercel will serve it.

    cd web
    python local_server.py

Then open http://localhost:8000 in the browser. Stop it with Ctrl+C.
It serves public/ as the site and the function in api/predict.py at /api/predict.
"""

import os
import sys
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "api"))
import predict  # loads the model once


class LocalHandler(predict.handler, SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path.split("?")[0] == "/api/predict":
            return predict.handler.do_GET(self)
        return SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self):
        if self.path.split("?")[0] == "/api/predict":
            return predict.handler.do_POST(self)
        self.send_error(404)

    def log_message(self, fmt, *args):
        pass


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8000"))
    handler = partial(LocalHandler, directory=os.path.join(HERE, "public"))
    print(
        f"model loaded ({len(predict.FEATURES)} features, {len(predict.CLASSES)} classes)"
    )
    print(f"open http://localhost:{port}   (Ctrl+C to stop)")
    ThreadingHTTPServer(("127.0.0.1", port), handler).serve_forever()
