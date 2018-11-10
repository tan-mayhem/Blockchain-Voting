#!/usr/bin/python

import signal
import SocketServer, socket
import threading
import time
import random
import sys
import json

class NodeList():
    myNodes = list()

    def add_node(self, host, port):
        self.myNodes.append([host, port])

    def set_nodes(self, nodes):
        self.myNodes = nodes

class ConnectionHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        text = self.request.recv(1024).strip()
        text_obj = json.loads(text)
        nodes = self.server.nodes
        nodes.add_node(text_obj["host"], text_obj["port"])
        json_obj = {}
        json_obj["nodes"] = nodes.myNodes
        self.request.sendall(json.dumps(json_obj))

def start_server(host, port, nodes):
    """
    start (single threaded) server - receive connections
    """
    server = SocketServer.ThreadingTCPServer(
        (host, port),
        ConnectionHandler,
    )
    server.nodes = nodes
    server.serve_forever()

def start_client(myHost, myPort, destHost, destPort, nodes):
    """
    start client - create connections
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((destHost, destPort))
    data = { "host": myHost, "port": myPort }
    s.sendall(json.dumps(data))
    r = s.recv(1024)
    r_data = json.loads(r)
    nodes.set_nodes(r_data.get("nodes"))
    print(nodes.myNodes)
    s.close()

def main():
    host = "localhost"
    port = None
    if len(sys.argv) == 2:
        port = int(sys.argv[1])
    else:
        port = int(raw_input("\tMy port: "))

    print("Serving {}:{}".format(host, port))

    nodes = NodeList()

    server_t = threading.Thread(
        target=start_server, args=(host, port, nodes)
    )
    server_t.daemon = True
    server_t.start()

    genesis = str(raw_input("Are you genesis? [y/N] ")) == "y"
    if not genesis:
        dHost = raw_input("Other host: ")
        dPort = int(raw_input("Other port: "))
        client_t = threading.Thread(
            target=start_client, args=(host, port, dHost, dPort, nodes),
        )
        client_t.daemon = True
        client_t.start()

    # Wait for ctrl-c interrupt
    try:
        signal.pause()
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
        main()
