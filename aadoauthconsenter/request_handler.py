import http.server
from .index_page import IndexPage
from .callback_page import CallbackPage


class RequestHandler(http.server.BaseHTTPRequestHandler):
    callback_page = CallbackPage()
    index_page = IndexPage()

    def do_GET(self):
        if self.path.startswith('/callback'):
            self.callback_page.do_GET(self)
        else:
            self.index_page.do_GET(self)

    def do_POST(self):
        self.index_page.do_POST(self)
