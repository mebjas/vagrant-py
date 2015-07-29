#!/usr/bin/env python

# TODO: change this with proper unit testing
# Code sample to test communication with daemon
# Via two named pipes

import os, time, sys

start = time.time()

#Make a connection to the daemon
print "init test process..."
randStr = "qwerty122"
o_pipename = "../tmp/pipe"
i_pipename = "../tmp/" +randStr
xmlfilepath = "/Users/minhazav/github/vagrant-pyd/test/sample.xml"

print "conecting to daemon via named pipe..."
outfifo = open(o_pipename, 'w+')

print "sending commadn to daemon...."
command = randStr +" create " +xmlfilepath +" "
outfifo.write(command)
outfifo.close()
print "command sent...."

print "creating listener pipe...."
# Now listen to a specific pipe
if not os.path.exists(i_pipename):
	os.mkfifo(i_pipename)


print "waiting for daemon to respond..."
i_fifo = open(i_pipename, 'r')
while True:
	line = i_fifo.readline()[:-1]
	if line:
		print '[%s] Output Recieved: %s' % (time.time(), line)
		os.unlink(i_pipename)
		break

print "time taken: %s" % (time.time() - start)
