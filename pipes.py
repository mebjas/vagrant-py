# Class to deal with pipes
class dpipes:
	name = "vagrantpyd_pipe"
	pipe = None

	def __init__(self):
		print "constructor for pipe called"
		print self.name
		self.pipe = open(self.name, 'r')


	def listen(self):
		while True:
			line = pipein.readline()[:-1]
	        data = 'Parent %d got "%s" at %s' % (os.getpid(), line, time.time( ))
	        with open("/Users/minhazav/hector/test/output.txt", "a") as testFile:
	        	testFile.write(data)