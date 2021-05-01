import parsing
import sys
# This file should contain code to receive either a document-id or word or both and output the required metrics. See the assignment description for more detail.

command = list(sys.argv)

if "--doc" in command:
    #print(command[2])
    parsing.result(command[2])