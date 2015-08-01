import unittest
import os
import sys
import inspect
import shutil

currentdir = os.path.dirname(
    os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

import daemon
import subprocess
import time
import json

# Global funcitions needed for testing


def isProcessRunning(pid):
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    else:
        return True

class TestDaemon(unittest.TestCase):

    def setUp(self):
        # Start the daemon
        self.currentdir = os.path.dirname(
            os.path.abspath(inspect.getfile(inspect.currentframe())))
        self.parentdir = os.path.dirname(self.currentdir)

        print "\n---- Starting Vagrant Daemon ----"
        subprocess.call([self.parentdir +'/main.py', 'start'])

    def tearDown(self):
        # Stop the Daemon
        print "\n---- Stopping Vagrant Daemon ----"
        subprocess.call([self.parentdir +'/main.py', 'stop'])


        # Do clean up tasks
        if os.path.exists(self.currentdir + "/tmp"):
            shutil.rmtree(self.currentdir + "/tmp")

    def test_daemon_active(self):
        # Get Process ID from ../tmp/process.pid file
        with open("../tmp/process.pid", 'r') as pf:
            pid = int(pf.read().strip())
            self.assertTrue(isProcessRunning(pid))

    def test_daemon_restart(self):
        print "\n---- Restarting Vagrant Daemon ----"
        subprocess.call([self.parentdir +'/main.py', 'restart'])
        with open("../tmp/process.pid", 'r') as pf:
            pid = int(pf.read().strip())
            self.assertTrue(isProcessRunning(pid))

    def test_communication(self):
        # Send a command via pipe
        # Make a connection to the daemon
        randStr = "qwerty122"
        o_pipename = "../tmp/pipe"
        i_pipename = "../tmp/" +randStr
        xmlfilepath = "/Users/minhazav/github/vagrant-pyd/test/sample.xml"
        outfifo = open(o_pipename, 'w+')
        command = randStr +" create " +xmlfilepath +" "
        outfifo.write(command)
        outfifo.close()

        # Now listen to a specific pipe
        if not os.path.exists(i_pipename):
            os.mkfifo(i_pipename)
        i_fifo = open(i_pipename, 'r')
        while True:
            line = i_fifo.readline()[:-1]
            if line:
                data = json.loads(line)

                self.assertEquals('', data['message']);
                self.assertFalse(data['error'])
                
                os.unlink(i_pipename)
                break



if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestDaemon)
    unittest.TextTestRunner(verbosity=2).run(suite)
