import time
from urlparse import parse_qs, urljoin
from urllib import unquote
import urllib2
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from SocketServer import ThreadingMixIn
import threading

HOST_NAME = 'localhost'
PORT_NUMBER = 8890

cache = {}

class MyHandler(BaseHTTPRequestHandler):
    def do_HEAD(self):
        """Respond to a HEAD request."""
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
    def do_GET(self):
        """Respond to a GET request."""
        opener = urllib2.build_opener()
        opener.addheaders = [('Accept', '*/*'), ('Host', 'localhost')]

        if self.path == "/is-alive":
            self.send_response(200)
            self.end_headers()
            self.wfile.close()
            return

        path_pieces = self.path.split('/')
        base_domain = unquote(path_pieces[1])
        path = "/".join(path_pieces[2:])

        if base_domain and path:
            url = base_domain + "/" + path
            if url in cache:
                response = cache[url]
                response_code = response['code']
                response_info = response['info']
                response_body = response['body']
            else:
                response = opener.open(url)
                response_info = response.info()
                response_body = response.read()
                response_code = response.getcode()
                cache[url] = {
                    "code": response_code,
                    "info": response_info,
                    "body": response_body
                }

            self.send_response(response_code)
            for header in response_info.headers:
                header_parts = header.split(':')
                self.send_header(header_parts[0], ":".join(header_parts[1:])[:-2])
            self.end_headers()
            self.wfile.write(response_body)
            self.wfile.close()
            return

        self.send_response(404)
        self.end_headers()


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""


if __name__ == '__main__':
    httpd = ThreadedHTTPServer((HOST_NAME, PORT_NUMBER), MyHandler)
    print time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER)

