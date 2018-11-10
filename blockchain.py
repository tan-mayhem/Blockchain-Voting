import hashlib
import time

class Block():
    def __init__(self, index, timeStamp, voterId, voterPassword, vote, previousHash):
        self.index = index
        self.timeStamp = timeStamp
        self.dayStamp = dayStamp
        self.voterId = voterId
        self.voterPassword = voterPassword
        self.vote = vote
        self.previousHash = previousHash
        self.currentHash = self.getCurrentHash()

    def getCurrentHash(self):
        sha = hashlib.sha256()
        sha.update = (str(self.index) + str(self.timeStamp) + str(self.dayStamp) + str(self.voterId) + str(self.voterPassword) + str(self.vote) + str(self.previousHash))
        return sha.hexdigest()

def createGenesisBlock():
    voterId = str(input("Enter your Voter ID: "))
    voterPassword = str(input("Enter your password: "))
    time.sleep(5)
    print()
    vote = str(input("Enter your vote: "))
    return Block(0, date.datetime.now(), voterId, voterPassword, vote, "0")
