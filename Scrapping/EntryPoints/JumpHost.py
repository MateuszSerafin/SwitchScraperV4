import paramiko
import re
from Scrapping.EntryPoints.EntryPointInterface import EntryPoint

class JumpHost(EntryPoint):

    client: paramiko.client.SSHClient
    connection: paramiko.channel.Channel

    def __init__(self, host, username, password = None, keyPath = None):
        self.client = paramiko.client.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        if(keyPath != None):
            self.client.connect(host, username=username, key_filename=keyPath)
        else:
            self.client.connect(host, username=username, password=password)
        self.connection = None

    def readAll(self, timeout=20) -> list[bytes]:
        #perhaps timeout shouln't be called like that but i leave it
        self.connection.settimeout(timeout)
        toReturn = bytes()
        try:
            while True:
                toReturn += self.connection.recv(999)
        except TimeoutError:
            return _removeANSI(toReturn).split(b"\n")

    def write(self, command: bytes):
        self.connection.send(command)

    def spawnNewShell(self) -> Exception:
        if(self.connection != None):
            self.connection.close()
        self.connection = self.client.invoke_shell()

def _removeANSI(inputBytes):
    regexForThat = re.compile(br'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    result = regexForThat.sub(b'', inputBytes)
    return result

