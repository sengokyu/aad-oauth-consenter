from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse


class CallbackPage:
    def do_GET(self, handler: BaseHTTPRequestHandler) -> None:
        query = urlparse(handler.path).query

        handler.send_response(200)
        handler.send_header('Content-Type', 'text/html;charset=utf-8')
        handler.end_headers()

        handler.wfile.write('<!DOCTYPE html>'.encode('utf-8'))

        for param in query.split('&'):
            handler.wfile.write(param.encode('utf-8'))
            handler.wfile.write('<br>'.encode('utf-8'))

        handler.wfile.flush()
