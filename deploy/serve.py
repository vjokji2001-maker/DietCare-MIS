"""Serve the Vite build under /diet with React Router fallback."""
import argparse
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit


class DietCareHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        self.serve(head_only=False)

    def do_HEAD(self):
        self.serve(head_only=True)

    def serve(self, head_only):
        requested = urlsplit(self.path)
        if requested.path == "/":
            self.send_response(302)
            self.send_header("Location", "/diet/" + ("?" + requested.query if requested.query else ""))
            self.end_headers()
            return
        if requested.path != "/diet" and not requested.path.startswith("/diet/"):
            self.send_error(404)
            return

        # Map the URL prefix to the dist root; retain the browser's query string.
        relative = requested.path[len("/diet"):].lstrip("/")
        self.path = "/" + relative
        target = Path(self.translate_path(self.path))
        if not relative or (not target.exists() and not Path(relative).suffix
                            and not relative.startswith("assets/")):
            self.path = "/index.html"
        if head_only:
            super().do_HEAD()
        else:
            super().do_GET()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--directory", default=str(Path(__file__).resolve().parent.parent / "dist"))
    parser.add_argument("--bind", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=8081)
    args = parser.parse_args()
    if not (Path(args.directory) / "index.html").is_file():
        parser.error("Build missing: run npm run build and select the dist directory.")
    handler = partial(DietCareHandler, directory=args.directory)
    print(f"Serving DietCare at http://{args.bind}:{args.port}/diet/", flush=True)
    ThreadingHTTPServer((args.bind, args.port), handler).serve_forever()
