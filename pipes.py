# Class to deal with pipes
import os, sys, time
from cmd import commandproc

class dpipes:
	def __init__(self, pipePath):
		self.pipePath = pipePath

	def create(self):
		# make a fifo pipe
		if not os.path.exists(self.pipePath):
			os.mkfifo(self.pipePath)

		print "[%s] Creating named pipe, to listen to incoming commands" % time.time()
		self.fifo = open(self.pipePath, 'r')

		while True:
			line = self.fifo.readline()[:-1]
			if line:
				print '[%s] Command Recieved: %s' % (time.time(), line)
				# Spawn a new thread and process the argument
				commandproc(line)

	def destroy(self):
		if os.path.exists(self.pipePath):
			os.remove(self.pipePath)