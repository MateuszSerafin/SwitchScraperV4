import subprocess
import time
import os

#THIS DOESN'T WORK YET
#I NEED TO CREATE PSEUDO TERMINAL FIRST AND THEN USE THIS OR SOMETHING LIKE THAT IT'S REALLY CLOSE TO WORKING
#TODO CLEAN IT UP BEFORE MAKING IT AVIABLE
'''

def _read(what: subprocess.Popen) -> list[bytes]:
    counter  = 0

    toReturn = []
    temporary = bytes("", "utf-8")
    while True:
        if(counter > 100):
            if(len(temporary) != 0):
                toReturn.append(temporary)
            return toReturn
        inPipe = what.stdout.read(1)

        if(inPipe == b'\n'):
            toReturn.append(temporary)
            temporary = bytes("", "utf-8")
            continue

        if(inPipe == b''):
            counter += 1
            continue
        if(inPipe == None):
            counter += 1
            continue

        temporary += inPipe


class SelfDevice():

    process: subprocess.Popen = None

    def readAll(self, timeout:int = 20) -> list[bytes]:
        if(self.process == None):
            raise Exception("This should not happen")

        time.sleep(timeout)
        toReturn = _read(self.process)

        if(len(toReturn) == 0):
            raise Exception("This is not expected")

        return toReturn

    def write(self, command: bytes):
        if(self.process == None):
            raise Exception("This should not happen")
        self.process.stdin.write(command)
        self.process.stdin.flush()

    def spawnNewShell(self) -> Exception:
        if(self.process != None):
            self.process.terminate()
            #probably won't be a bad thing to do
            time.sleep(1)

        self.process = subprocess.Popen('cmd.exe',
                                      stdin=subprocess.PIPE,
                                      stdout=subprocess.PIPE,
                                      stderr=subprocess.PIPE, shell=True)

        os.set_blocking(self.process.stdout.fileno(), False)
        #subprocess needs sometime to think and initialize
        #don't remove it

        time.sleep(5)
'''