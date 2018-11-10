#!/usr/bin/python

import signal
import SocketServer, socket
import threading
import time
import random

class DisplayHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        text = self.request.recv(1024).strip()
        print("{} wrote: {}".format(
            self.client_address[0], text,
        ))

def start_server(host, port):
    """
    start (single threaded) server - receive connections
    """
    SocketServer.TCPServer(
        (host, port),
        DisplayHandler,
    ).serve_forever()

def start_client(host, port):
    """
    start client - create connections
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    data = str(time.time())
    s.sendall(data)
    s.close()

def main(host, port):
    print("Serving {}:{}".format(host, port))

    server_t = threading.Thread(
        target=start_server, args=(host, port)
    )
    server_t.daemon = True
    server_t.start()

    client_t = threading.Thread(
        target=start_client, args=(host, port),
    )
    client_t.daemon = True
    client_t.start()

    # Wait for ctrl-c interrupt
    try:
        signal.pause()
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main("localhost", random.randint(12345, 55555))
