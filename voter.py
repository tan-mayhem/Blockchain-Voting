#!/usr/bin/python

import signal
import SocketServer, socket
import threading
import time
import random
import sys
import json
import Queue

from blockchain import Block, createGenesisBlock, next_block_from_array

bc = list()
q_bc = Queue.Queue()

nodes = list()
q_nodes = Queue.Queue()

class ConnectionHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        # Add connected host and port to list of clients
        text = self.request.recv(1024).strip()
        text_obj = json.loads(text)

        #nodes = self.server.nodes
        #bc = self.server.bc
        nodes = self.server.q_nodes.get()
        bc = self.server.q_bc.get()
        if text_obj["type"] == "get_blockchain":
            nodes.append((text_obj["host"], text_obj["port"]))
            json_obj = {}
            json_obj["nodes"] = nodes
            print("Requested nodes: " + str(nodes))
            json_obj["blockchain"] = bc
            print("Requested blockchain: " + str(bc))
            self.request.sendall(json.dumps(json_obj))
            q_nodes.put(nodes)
            q_bc.put(bc)
        elif text_obj["type"] == "add_vote":
            nodes = text_obj["nodes"][:]
            # TODO: approve vote
            print("Updated nodes: " + str(nodes))
            bc.append(text_obj["vote"])
            print("Updated bc: " + str(bc))
            q_nodes.put(nodes)
            q_bc.put(bc)

def start_server(host, port, q_nodes, q_bc):
    """
    start (single threaded) server - receive connections
    """
    server = SocketServer.ThreadingTCPServer(
        (host, port),
        ConnectionHandler,
    )
    #server.nodes = q_nodes.get()
    #server.bc = q_bc.get()
    server.q_nodes = q_nodes
    server.q_bc = q_bc
    server.serve_forever()

def send_blockchain_to_network(b, nodes):
    for i in range(0, len(nodes)-1):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((nodes[i][0], nodes[i][1]))

        data = { "type": "add_vote", "vote": b, "nodes": nodes }
        s.sendall(json.dumps(data))
        s.close()

def start_client(myHost, myPort, destHost, destPort, q_nodes, q_bc):
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
    b = next_block_from_array(bc[-1]).block_to_array()
    bc.append(b)
    print("client recieved bc: " + str(bc))
    print("client recieved nodes: " + str(nodes))

    s.close()
    
    q_nodes.put(nodes)
    q_bc.put(bc)
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
        target=start_server, args=(host, port, q_nodes, q_bc)
    )
    server_t.daemon = True
    server_t.start()

    genesis = str(raw_input("Are you genesis? [y/N] ")) == "y"
    if genesis:
        b = createGenesisBlock()
        bc.append(b.block_to_array())
        q_bc.put(bc)
        q_nodes.put(nodes)
    else:
        dHost = raw_input("Other host: ")
        dPort = int(raw_input("Other port: "))
        client_t = threading.Thread(
            target=start_client, args=(host, port, dHost, dPort, q_nodes, q_bc),
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
