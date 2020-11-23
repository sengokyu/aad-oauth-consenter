import http.server
from urllib.parse import parse_qs, quote
import webbrowser

PORT = 8072
INDEX_PAGE = '''<!DOCTYPE html>
        <style>input{width:60em;}</style>
        <form method="POST">
        <p>Tenant domain name: <input name="tenant" placeholder="sample.onmicrosoft.com">
        <p>Application ID: <input name="application_id">
        <p>List of scope (space separated): <input name="scope" placeholder="user.read">
        <p><input type="submit">
        </form>
        '''

class RequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith('/callback'):
            self.__receive_callback()
        else:
            self.__serve_index()

    def do_POST(self):
        self.__redirect_to_authorize()

    def __redirect_to_authorize(self):
        (tenant, application_id, scope) = self.__parse_input()
        url = self.__create_url(tenant, application_id, scope)

        self.send_response(303)
        self.send_header('Location', url)
        self.end_headers()

    def __parse_input(self):
        content_length = int(self.headers.get('Content-Length', 0))
        input_str = self.rfile.read(content_length).decode('utf-8')
        input = parse_qs(input_str)
        return (input['tenant'][0], input['application_id'][0], input['scope'][0])

    def __create_url(self, tenant, application_id, scope):
        redirect_uri = 'http://localhost:%s/callback' % PORT
        url = ('https://login.microsoftonline.com/%s/oauth2/v2.0/authorize'
               '?response_type=code'
               '&redirect_uri=%s'
               '&response_mode=query'
               '&scope=%s'
               '&client_id=%s') % (
                   tenant,
                   quote(redirect_uri),
                   quote(scope),
                   quote(application_id)
        )
        return url

    def receive_callback(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/html;charset=utf-8')
        self.end_headers()

    def __serve_index(self) -> None:
        self.send_response(200)
        self.send_header('Content-Type', 'text/html;charset=utf-8')
        self.end_headers()
        self.wfile.write(INDEX_PAGE.encode('utf-8'))
        self.wfile.flush()


if __name__ == '__main__':
    with http.server.HTTPServer(('', PORT), RequestHandler) as server:
        print('Press Ctrl-C to stop the server.')
        webbrowser.open('http://localhost:%s' % PORT)
        server.serve_forever()
