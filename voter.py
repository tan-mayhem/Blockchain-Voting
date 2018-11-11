#!/usr/bin/python

import signal
import SocketServer, socket
import threading
import time
import random
import sys
import json

from blockchain import Block, createGenesisBlock, next_block_from_array

bc = list()
nodes = list()

class ConnectionHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        # Add connected host and port to list of clients
        text = self.request.recv(1024).strip()
        text_obj = json.loads(text)

        nodes = self.server.nodes
        bc = self.server.bc
        if text_obj["type"] == "get_blockchain":
            nodes.append((text_obj["host"], text_obj["port"]))
            json_obj = {}
            json_obj["nodes"] = nodes
            print(nodes)
            json_obj["blockchain"] = bc
            print(bc)
            self.request.sendall(json.dumps(json_obj))
        elif text_obj["type"] == "add_vote":
            nodes = text_obj["nodes"][:]
            # TODO: approve vote
            bc.append(text_obj["vote"])
            print(bc)

def start_server(host, port):
    """
    start (single threaded) server - receive connections
    """
    server = SocketServer.ThreadingTCPServer(
        (host, port),
        ConnectionHandler,
    )
    server.nodes = nodes
    server.bc = bc
    server.serve_forever()

def send_blockchain_to_network(b, nodes):
    print(nodes)
    for i in range(0, len(nodes)-1):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((nodes[i][0], nodes[i][1]))

        data = { "type": "add_vote", "vote": b, "nodes": nodes }
        s.sendall(json.dumps(data))
        s.close()

def start_client(myHost, myPort, destHost, destPort):
    """
    start client - create connections
    """
    # Make connection
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((destHost, destPort))

    # Send my hostname and port
    data = { "type": "get_blockchain", "host": myHost, "port": myPort }
    s.sendall(json.dumps(data))

    # Receive list of nodes in network and blockchain
    r = s.recv(1024)
    r_data = json.loads(r)
    nodes = r_data.get("nodes")[:]
    bc = (r_data.get("blockchain"))
    print(bc)
    b = next_block_from_array(bc[-1]).block_to_array()
    bc.append(b)

    s.close()
    
    send_blockchain_to_network(b, nodes)

def main():
    host = "localhost"
    port = None
    if len(sys.argv) == 2:
        port = int(sys.argv[1])
    else:
        port = int(raw_input("\tMy port: "))

    print("Serving {}:{}".format(host, port))
    nodes.append((host, port))

    server_t = threading.Thread(
        target=start_server, args=(host, port)
    )
    server_t.daemon = True
    server_t.start()

    genesis = str(raw_input("Are you genesis? [y/N] ")) == "y"
    if genesis:
        b = createGenesisBlock()
        bc.append(b.block_to_array())
    else:
        dHost = raw_input("Other host: ")
        dPort = int(raw_input("Other port: "))
        client_t = threading.Thread(
            target=start_client, args=(host, port, dHost, dPort),
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
