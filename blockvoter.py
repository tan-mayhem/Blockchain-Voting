import datetime
import time

def returncurrentdate():
	now = datetime.datetime.now()
	return now

c = returncurrentdate() 
time.sleep(1)
d = returncurrentdate() 

print(c) 

print(d) 
