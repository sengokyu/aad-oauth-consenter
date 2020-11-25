from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs, quote

INDEX_PAGE = '''<!DOCTYPE html>
        <style>input{width:60em;}</style>
        <form method="POST">
        <p>Tenant domain name: <input name="tenant" placeholder="sample.onmicrosoft.com">
        <p>Application ID: <input name="application_id">
        <p>List of scope (space separated): <input name="scope" placeholder="user.read">
        <p><input type="submit">
        </form>
        '''


class IndexPage:
    def do_GET(self, handler: BaseHTTPRequestHandler) -> None:
        handler.send_response(200)
        handler.send_header('Content-Type', 'text/html;charset=utf-8')
        handler.end_headers()
        handler.wfile.write(INDEX_PAGE.encode('utf-8'))
        handler.wfile.flush()

    def do_POST(self, handler: BaseHTTPRequestHandler) -> None:
        port = handler.server.server_address[1]
        (tenant, application_id, scope) = self.__parse_input(handler)
        url = self.__create_url(port, tenant, application_id, scope)

        handler.send_response(303)
        handler.send_header('Location', url)
        handler.end_headers()

    def __parse_input(self, handler: BaseHTTPRequestHandler):
        input = parse_qs(self.__read_content(handler))
        return (input['tenant'][0], input['application_id'][0], input['scope'][0])

    def __create_url(self, port, tenant, application_id, scope) -> str:
        redirect_uri = 'http://localhost:%s/callback' % port
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

    def __read_content(self, handler: BaseHTTPRequestHandler) -> str:
        content_length = int(handler.headers.get('Content-Length', 0))
        return handler.rfile.read(content_length).decode('utf-8')
