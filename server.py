import http.server
import socketserver
import argparse
import logging

class Config:
    WEBGL_BUILD_DIR = "./"
    DEFAULT_PORT = 1234
    PROJECT_SUBDIR = "Project"

class RedirectHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(301)
            self.send_header('Location', f'/{Config.PROJECT_SUBDIR}/')
            self.end_headers()
            return
        return super().do_GET()

def run_server(port):
    handler = RedirectHandler

    with socketserver.TCPServer(("", port), handler) as httpd:
        logging.info(f"Serving at http://localhost:{port}/ (redirects to /{Config.PROJECT_SUBDIR}/)")
        logging.info("Press Ctrl+C to stop the server.")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            logging.info("\nServer stopped.")
            httpd.server_close()
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            httpd.server_close()

def main():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

    # Argument parser
    parser = argparse.ArgumentParser(description="Serve a Unity WebGL game on a local server.")
    parser.add_argument(
        "--port", type=int, default=Config.DEFAULT_PORT, help="Port to serve the game on (default: 1234)"
    )
    args = parser.parse_args()

    run_server(args.port)

if __name__ == "__main__":
    main()
