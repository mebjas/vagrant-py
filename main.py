''' Code to test adding a vagrant box by command line arg'''
import sys

args = sys.argv;
# 1st argument would be script name so ignore

if (args[1] == "-a"):
	if (len(args) >= 2):
		from subprocess import call
		call(["vagrant", "box adding " +args[2]])
	else:
		print("insufficient arguments")