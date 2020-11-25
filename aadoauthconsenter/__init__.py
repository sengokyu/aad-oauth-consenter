import http.server
import webbrowser
from .request_handler import RequestHandler

def main(port):
    with http.server.HTTPServer(('', port), RequestHandler) as server:
        print('Press Ctrl-C to stop the server.')
        webbrowser.open('http://localhost:%s' % port)
        server.serve_forever()
