## Module to obtain packet data from a pcap/dump file
## and save it in csv format using tshark.
## Filenames of input pcap files are taken from InputFiles.txt
## Tshark options are present in TsharkOptions.txt
## TsharkOptions.txt should not contain the -r option.

## usage: python FilterPackets.py

#import global constants
from P2P_CONSTANTS import *
from FilterPacketsHelper import *
import multiprocessing as MP
import subprocess

#execute a shell command as a child process
def executeCommand(command,outfilename):
        sem.acquire()

        subprocess.call(command, shell = True)
	
        with open(outfilename, 'r') as infile:
            data = [eachline.strip() for eachline in infile]
	
        data = preprocess(data)
	
        with open(outfilename,'w') as outfile:
            for eachcomponent in data:
                outfile.write(eachcomponent)
	
        print 'done processing : ' + outfilename
        sem.release()

#obtain input parameters and pcapfilenames
inputfiles = getPCapFileNames()
tsharkOptions = getTsharkOptions()

#create a semaphore so as not to exceed threadlimit
sem = MP.Semaphore(THREADLIMIT)

#get tshark commands to be executed
for filename in inputfiles:
        print filename
        (command,outfilename) = contructTsharkCommand(filename,tsharkOptions)
        task = MP.Process(target = executeCommand, args = (command, outfilename,))
        task.start()
