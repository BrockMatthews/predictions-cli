import time
import requests
from webbrowser import open as open_url
from random import getrandbits

from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs


CLIENT_ID = 'fa9i0kafxhhd6681fe99wmg7pid0fq'



def get_auth_token() -> str | None:
    state = f'{getrandbits(128):032x}'

    token = None
    wait = True

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            nonlocal token, wait
            wait = False

            if len(self.path) <= 1:
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(b'<html><head><title>Predictions Manager CLI</title><script>url=window.location.href;if(url.includes("#"))window.location.replace(url.replace("#","?"))</script></head><body><h1>Please replace the first # in the url with a ? and follow the link.</h1></body></html>')
                wait = True
                return

            if self.path.startswith('/favicon.ico'):
                wait = True
                return

            query = parse_qs(urlparse(self.path).query)
            if 'state' not in query or query['state'][0] != state:
                self.send_response(400)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(b'<html><head><title>Bad Request - Predictions Manager CLI</title></head><body><h1>State returned from Twitch does not match state sent.</h1></body></html>')
                return

            if 'error' in query:
                self.send_response(400)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(f'<html><head><title>Error - Predictions Manager CLI</title></head><body><h1>{query["error"][0]}</h1><p>{query["error_description"][0]}</p></body></html>'.encode('utf-8'))
                return

            if 'access_token' not in query:
                self.send_response(400)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(b'<html><head><title>Bad Request - Predictions Manager CLI</title></head><body><h1>Access token not returned from Twitch.</h1></body></html>')
                return

            token = query['access_token'][0]

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'<html><head><title>Success - Predictions Manager CLI</title></head><script>window.open("","_self").close()</script><body><h1>Authentication success!</h1><p>You can close this window now.</p></body></html>')


    server = HTTPServer(('localhost', 3000), Handler)
    server.timeout = 120

    open_url(f"https://id.twitch.tv/oauth2/authorize?response_type=token&client_id={CLIENT_ID}&redirect_uri=http://localhost:3000&scope=channel%3Amanage%3Apredictions&state={state}")

    # Listen on localhost:3000 for the redirect
    while token is None and wait:
        start_time = time.time()
        server.handle_request()

        # If the server times out, break out of the loop
        if time.time() - start_time >= server.timeout:
            break

    server.server_close()

    return token



def get_broadcaster_id(token: str) -> str | None:

    response = requests.get('https://api.twitch.tv/helix/users', headers={'Authorization': f'Bearer {token}', 'Client-Id': CLIENT_ID})
    if response.status_code != 200:
        return None

    return response.json()['data'][0]['id']



if __name__ == '__main__':
    token = get_auth_token()
    if token is None:
        print('Authentication failed.')
        exit(1)
    print(f'Authentication successful. Token: {token}')

    broadcaster_id = get_broadcaster_id(token)
    if broadcaster_id is None:
        print('Failed to get broadcaster ID.')
        exit(1)
    print(f'Broadcaster ID: {broadcaster_id}')