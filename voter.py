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
from userauth import enter

bc = list()
q_bc = Queue.Queue()

nodes = list()
q_nodes = Queue.Queue()

winnerarr = [] 
candidateNames = []
q_cand = Queue.Queue()
#for i in range(5) :
#	winnerarr.append(0)

class ConnectionHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        # Add connected host and port to list of clients
        text = self.request.recv(1024).strip()
        text_obj = json.loads(text)

        nodes = self.server.q_nodes.get()
        bc = self.server.q_bc.get()
        candidateNames = self.server.q_cand.get()
        if text_obj["type"] == "get_blockchain":
            nodes.append((text_obj["host"], text_obj["port"]))
            json_obj = {}
            json_obj["nodes"] = nodes
            print("Requested nodes: " + str(nodes))
            json_obj["blockchain"] = bc
            print("Requested blockchain: " + str(bc))
            json_obj["candidateNames"] = candidateNames
            self.request.sendall(json.dumps(json_obj))
        elif text_obj["type"] == "add_vote":
            nodes = text_obj["nodes"][:]
            if enter(text_obj["vote"][1], text_obj["vote"][2], bc):
                print("Updated nodes: " + str(nodes))
                bc.append(text_obj["vote"])
                print("Updated bc: " + str(bc))
            else:
                print("Warning: invalid user submitted vote. Not adding to blockchain...")
        q_nodes.put(nodes)
        q_bc.put(bc)
        q_cand.put(candidateNames)

def start_server(host, port, q_nodes, q_bc, q_cand):
    """
    start (single threaded) server - receive connections
    """
    server = SocketServer.ThreadingTCPServer(
        (host, port),
        ConnectionHandler,
    )
    server.q_nodes = q_nodes
    server.q_bc = q_bc
    server.q_cand = q_cand
    server.serve_forever()

def send_blockchain_to_network(b, nodes):
    for i in range(0, len(nodes)-1):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((nodes[i][0], nodes[i][1]))

        data = { "type": "add_vote", "vote": b, "nodes": nodes }
        s.sendall(json.dumps(data))
        s.close()

def start_client(myHost, myPort, destHost, destPort, q_nodes, q_bc, q_cand):
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

    if enter(b[1], b[2], bc):
        print("client recieved bc: " + str(bc))
        print("client recieved nodes: " + str(nodes))
        candidateNames = r_data.get("candidateNames")[:]

        s.close()
        
        q_nodes.put(nodes)
        q_bc.put(bc)
        q_cand.put(candidateNames)
        send_blockchain_to_network(b, nodes)
    else:
        print("Warning: you are not a valid voter")
        sys.exit()

def checkwinner(names):
	bc = q_bc.get() 
	for i in range(0,len(bc)):
		a = int(bc[i][3]) - 1
		winnerarr[a] = winnerarr[a] + 1
	max = -1
        winner = -1
	for j in range(0,len(winnerarr)):
	    if winnerarr[j] > max:
                max = winnerarr[j]
                winner = j

	print "The winner is candidate number : " + str((winner+1))  + " Namely : " + names[winner] 

def initializecandidates():
	n = input("Enter the number of candidates : ")
	for l in range(n):
		winnerarr.append(0)
	print winnerarr
	for m in range(0,n):
		bleh = str(raw_input("candidate number " + str(m) + "\'s name : "))
		candidateNames.append(bleh)
	print "The candidates are : " 
	for p in range(0,n):
		print str(p+1) + ". "  + candidateNames[p] 	
        q_cand.put(candidateNames)

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
        target=start_server, args=(host, port, q_nodes, q_bc, q_cand)
    )
    server_t.daemon = True
    server_t.start()

    genesis = str(raw_input("Are you genesis? [y/N] ")) == "y"
    if genesis:
        initializecandidates()
        b = createGenesisBlock().block_to_array()
        bc.append(b)
        if enter(b[1], b[2], bc):
            q_bc.put(bc)
            q_nodes.put(nodes)
        else:
            print("Warning: you are not a valid voter")
            sys.exit()
    else:
        dHost = raw_input("Other host: ")
        dPort = int(raw_input("Other port: "))
        client_t = threading.Thread(
            target=start_client, args=(host, port, dHost, dPort, q_nodes, q_bc, q_cand),
        )
        client_t.daemon = True
        client_t.start()

    # Wait for ctrl-c interrupt
    try:
    	while True:
        	time.sleep(1) ;
    except KeyboardInterrupt:
        pass

    candidateNames = q_cand.get()
    for i in range(len(candidateNames)):
            winnerarr.append(0)
    checkwinner(candidateNames)


if __name__ == "__main__":
        main()
