#!/usr/bin/env python
 
import sys, time
from daemon import daemon
from pipes import dpipes
 
pidFilePath = "/Users/minhazav/hector/test/test.pid"
logfilePath = "/Users/minhazav/hector/test/logs"
errfilePath = "/Users/minhazav/hector/test/err"

class vagrantpyd(daemon):
    def run(self):
        #TODO: define event listener for named pipe here
        # Currently writing to temp code to test daemon for now
        try:
            mypipe = dpipes()
        except Exception as inst:
            print "exception occured while trying to create a log file"
            print inst
        while True:
            print "something printed to stdout"
            time.sleep(1)
 

if __name__ == "__main__":
    daemon = vagrantpyd(pidFilePath, logfilePath, errfilePath)
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            print "Vagrantpyd starting..."
            daemon.start()
        elif 'stop' == sys.argv[1]:
            print "Vagrantpyd stopping..."
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            print "Vagrantpyd restarting..."
            daemon.restart()
        else:
            print "Unknown command"
            sys.exit(2)
        
        sys.exit(0)
    else:
        print "usage: %s start|stop|restart" % sys.argv[0]
        sys.exit(2)