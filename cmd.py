# Code to deal with the requested command
import os
import sys
import time
import json
import data
import subprocess
import shutil
from threading import Thread
from data import vagrantData


class helper:

    @staticmethod
    # Global function to copy file or directory
    def copy(src, dest):
        try:
            shutil.copytree(src, dest)
        except OSError as e:
            # If the error was caused because the source wasn't a directory
            if e.errno == errno.ENOTDIR:
                shutil.copy(src, dest)
            else:
                print('Directory not copied. Error: %s' % e)

    @staticmethod
    def getRootFolder(path):
        arr = path.split('/')
        if arr[0] == '':
            try:
                return arr[1]
            except:
                return ''
        return arr[0]


class commandproc:

    # Defining the main output variable to be sent back to the
    # system. It will be passed by reference to all classes
    out = {}

    # Function to add a vagrant box if not exists
    def vagrantAddBox(self, boxname):
        try:
            op = subprocess.check_call(
                ['vagrant', 'box', 'add', boxname])
        except Exception as ex:
            print """[%s] Exception Occured while adding box {%s},
            Ex: {%s}""" % (time.time(), boxname, ex)

    # Function to call init method in the current directory
    def vagrantInit(self):
        try:
            op = subprocess.check_output(['vagrant', 'init'])
        except Exception as ex:
            print """[%s] Exception Occured while initialising vagrant box,
            Ex: {%s}""" % (time.time(), ex)

            return False

        return True

    def classifier(self, command):
        args = command.split(' ')

        if len(args) < 3:
            print """[%s] Invalid command: {%s} sent to daemon.
			Skipping the command!""" % (time.time(), command)
            return

        self.outPipe = self.currentPath + "/tmp/" + args[0]

        # Init entries to out dictionery
        self.out['error'] = False
        self.out['message'] = ''

        # ------------------------------------------------------------------------
        # Code to preform requested action
        # ------------------------------------------------------------------------

        cmdString = args[1]
        if "create" == cmdString:
            """
            TASK - read xml file and create a box,return meaning full information
            """

            challengePath = args[2]
            xmlFile = challengePath + "/challenge.xml"
            # TODO verify the type of data ^
            xmlData = vagrantData(xmlFile)
            success = xmlData.parse()
            if success is not True:
                self.out['error'] = True
                self.out['message'] = """Unable to parse provided XML!
				Error: %s """ % str(success)
            else:
                # TODO: verify the data loaded from XML
                data = {}
                data['basebox'] = xmlData.baseBox
                data['basePath'] = self.currentPath + "/data/boxes"

                # Add a base box if not exists
                self.vagrantAddBox(xmlData.baseBox)

                # Create a challenge directory
                os.chdir(self.currentPath)
                if not os.path.exists("./data"):
                    print "making dir ./data"
                    op = subprocess.check_output(['pwd'])
                    print op
                    os.makedirs("./data")

                os.chdir("./data")
                if not os.path.exists("./boxes"):
                    os.makedirs("./boxes")
                os.chdir("./boxes")

                challengeIdBase = xmlData.baseBox.replace('/', '_')
                i = 1
                challengeId = challengeIdBase + str(i)
                while os.path.exists(challengeId):
                    i += 1
                    challengeId = challengeIdBase + str(i)

                data['challengeId'] = challengeId
                os.makedirs(challengeId)
                os.chdir("./" + challengeId)

                # Init vagrant at that directory
                if not self.vagrantInit():
                    self.out['error'] = True
                    self.out['message'] = 'vagrant init failed'
                else:
                    shutil.copyfile(xmlFile, "challenge.xml")
                    # create the files directory and copy the files, to that directory
                    # In same manner as provided in xml
                    os.makedirs("files")
                    os.chdir("./files")
                    directoriesCopies = []

                    # Copy the files
                    for _file in xmlData.files:
                        if helper.getRootFolder(_file.src) not in directoriesCopies:
                            # Copy that folder to this folder
                            directory = helper.getRootFolder(_file.src)
                            helper.copy(
                                challengePath + "/" + directory, directory)
                            directoriesCopies.append(directory)

                    # Copy the scripts
                    for _script in xmlData.scripts:
                        if helper.getRootFolder(_script) not in directoriesCopies:
                            # Copy that folder to this folder
                            directory = helper.getRootFolder(_script)
                            helper.copy(
                                challengePath + "/" + directory, directory)
                            directoriesCopies.append(directory)

                    # TODO: Modify the vagrantFile according to xml data
                    self.out['data'] = data
                    self.out['message'] = 'success'

        elif "start" == cmdString:
            print "start command triggered"
            # TASKS:
            # Create a clone directory of the challenge directory
            # Start VagrantBox for this one
            # Return the ID
        elif "stop" == cmdString:
            print "stop command triggered"
        elif "info" == cmdString:
            if "all" == args[2]:
                if "box" == args[3]:

                    # Code to list all boxes in system
                    op = subprocess.check_output(['vagrant', 'box', 'list'])
                    op_arr = op.split('\n')
                    if len(op_arr) > 0:
                        del op_arr[-1]

                    self.out['data'] = op_arr
                    self.out['message'] = 'success'

                elif "challenge" == args[3]:
                    print "info all challenge called"
            elif "box" == args[2]:
                boxId = args[3]
                print "info box <box id> called"
            elif "challenge" == args[2]:
                challengeId = args[3]
                print "info challenge <challenge id> called"

        # ------------------------------------------------------------------------
        # Code to respond back to the client
        # ------------------------------------------------------------------------
        print "responding back via client"
        # make a output fifo pipe
        if not os.path.exists(self.outPipe):
            os.mkfifo(self.outPipe)

        output = json.dumps(self.out) + ' '

        self.outfifo = open(self.outPipe, 'w+')
        self.outfifo.write(output)
        self.outfifo.close()
        print """[%s] Output sent back to client using pipe:
		%s""" % (time.time(), self.outPipe)

    # Constructor: Calls the classifier method in new thread
    def __init__(self, command):
        self.currentPath = os.path.dirname(os.path.realpath(__file__))
        thrd = Thread(target=self.classifier, args=(command, ))
        thrd.start()
