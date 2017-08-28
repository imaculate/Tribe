from http.server import HTTPServer, BaseHTTPRequestHandler
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.request import urlopen, HTTPError
from webbrowser import open_new

REDIRECT_URL = 'http://localhost:8080/'

class HTTPServerHandler(BaseHTTPRequestHandler):

    """
    HTTP Server callbacks to handle Facebook OAuth redirects
    """
    def __init__(self, request, address, server, a_id, a_secret):
        self.app_id = a_id
        self.app_secret = a_secret
        super().__init__(request, address, server)

    def get_access_token_from_url(url):
        """
        Parse the access token from Facebook's response
        Args:
            uri: the facebook graph api oauth URI containing valid client_id,
                 redirect_uri, client_secret, and auth_code arguements
        Returns:
            a string containing the access key
        """
        token = str(urlopen(url).read(), 'utf-8')
        return token.split('=')[1].split('&')[0]

    def do_GET(self):
        GRAPH_API_AUTH_URI = ('https://graph.facebook.com/v2.2/oauth/'
            + 'access_token?client_id=' + self.app_id + '&redirect_uri='
            + REDIRECT_URL + '&client_secret=' + self.app_secret + '&code=')

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        if 'code' in self.path:
            self.auth_code = self.path.split('=')[1]
            #Display to the user that they no longer need the browser window
            self.wfile.write(bytes('<html><h1>You may now close this window.'
                              + '</h1></html>', 'utf-8'))
            self.server.access_token = self.get_access_token_from_url(GRAPH_API_AUTH_URI + self.auth_code)



class TokenHandler:
    """
    Class used to handle Facebook oAuth
    """
    def __init__(self, a_id, a_secret):
        self._id = a_id
        self._secret = a_secret

    def get_access_token(self):
        ACCESS_URI = ('https://www.facebook.com/dialog/'
            + 'oauth?client_id=' +self._id + '&redirect_uri='
            + REDIRECT_URL + "&scope=xxxxx")

        open_new(ACCESS_URI)
        httpServer = HTTPServer(('localhost', 8080),
                lambda request, address, server: HTTPServerHandler(request, address, server, self._id, self._secret))
        httpServer.handle_request()
        return httpServer.access_token
