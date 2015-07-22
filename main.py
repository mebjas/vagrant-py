#!/usr/bin/env python
 
import sys, time
from daemon import daemon
 
processInfoFilePath = "/Users/minhazav/hector/test/test.pid"
outputFilePath = "/Users/minhazav/hector/test/output.txt"   #TODO: remove this

class vagrantpyd(daemon):
    def run(self):
        #TODO: define event listener for named pipe here
        # Currently writing to temp code to test daemon for now
        while True:
            with open(outputFilePath, "a") as testFile:
                testFile.write("adding test text.\n")
            time.sleep(1)
 

if __name__ == "__main__":
    daemon = vagrantpyd(processInfoFilePath)
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        else:
            print "Unknown command"
            sys.exit(2)
            
        print "Vagrantpyd %sed Successfully. Connect using named pipes." % sys.argv[1]
        
        sys.exit(0)
    else:
        print "usage: %s start|stop|restart" % sys.argv[0]
        sys.exit(2)