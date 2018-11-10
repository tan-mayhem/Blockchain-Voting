import hashlib
import time
import datetime as date

class Block:
    def __init__(self, index, timeStamp, voterId, voterPassword, vote, previousHash):
        self.index = index
        self.timeStamp = timeStamp
        self.voterId = voterId
        self.voterPassword = voterPassword
        self.vote = vote
        self.previousHash = previousHash
        self.currentHash = self.getCurrentHash()

    def getCurrentHash(self):
        sha = hashlib.sha256(str(self.index) + str(self.timeStamp) + str(self.voterId) + str(self.voterPassword) + str(self.vote) + str(self.previousHash))
        return sha.hexdigest()

def createGenesisBlock():
    voterId = raw_input("Enter your Voter ID: ")
    voterPassword = raw_input("Enter your password: ")
    time.sleep(1)
    print "Candidates for the House"
    print "Index " + " Name "
    print "1. " + " Person 1 "
    print "2. " + " Person 2 "
    print "3. " + " Person 3 "
    print "4. " + " Person 4 "
    print "5. " + " Person 5 "
    vote = raw_input("Enter your vote: ")
    return Block(0, date.datetime.now(), voterId, voterPassword, vote, "0")

def next_block(last_block):
    voterId = raw_input("Enter your Voter ID: ")
    voterPassword = raw_input("Enter your password: ")
    time.sleep(1)
    print "Candidates for the House"
    print "Index " + " Name "
    print "1. " + " Person 1 "
    print "2. " + " Person 2 "
    print "3. " + " Person 3 "
    print "4. " + " Person 4 "
    print "5. " + " Person 5 "
    vote = raw_input("Enter your vote: ")
    this_index = last_block.index + 1
    this_timestamp = date.datetime.now()
    previousHash = last_block.currentHash
    return Block(this_index, this_timestamp, voterId, voterPassword, vote, previousHash)

blockchain = []
blockchain.append(createGenesisBlock())
previous_block = blockchain[0]

number_blocks = 20

for i in range(0, number_blocks):
  block_to_add = next_block(previous_block)
  blockchain.append(block_to_add)
  previous_block = block_to_add
  print "Block #{} has been added to the blockchain!".format(block_to_add.index)
  print "Hash: {}\n".format(block_to_add.currentHash)
  print blockchain
