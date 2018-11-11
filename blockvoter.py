import hashlib

class Block:
	def next_block(last_block):
		voterId = str(input("Enter your Voter ID "))
		voterPassword = str(input("Enter your password: "))
		time.sleep(5)
		print()
		vote = str(input("Enter your vote: "))
		this_index = last_block.index + 1
		this_timestamp = date.datetime.now() 
		#this_data = "Voter Number : " + str(this_index) 
		previousHash = last_block.currentHash
		return Block(this_index,this_timestamp, voterId, voterPassword, vote, previousHash)

#voterid voterPassword vote previousHash