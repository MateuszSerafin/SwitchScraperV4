from Scrapping.Authentication.SSHKey import SSHKeyAuth
from Scrapping.Authentication.Telnet import Telnet
from Scrapping.EntryPoints.EntryPointInterface import EntryPoint
from Scrapping.EntryPoints.JumpHost import JumpHost
import time
import threading

#In my testing lab
#10.21.37.2 is GNS3 server
#192.168.122.182 is Linux VM inside of project
#10.0.0.2 -> TelnetNoPassword
#10.0.0.3 -> TelentOnlyPassword
#10.0.0.4 -> TelnetUserPassword
#10.0.0.5 -> SSHKey
#10.0.0.6 -> SSHUserPassword
#All switches have the same users and password (User, Password1)

def validateLastLine(entry: EntryPoint, expectedLastLine: str):
    entry.write(bytes("\n", "utf-8"))
    output = entry.readAll(timeout=5)
    if (output[0] != b'\r' or bytes(expectedLastLine, "utf-8") not in output[1]):
        print(output)
        raise Exception("Authed doesn't match what is expected")


def theoreticallyAllCases(entry: EntryPoint, host, expectedLastLine: str):
    entry.spawnNewShell()
    telnet = Telnet(entry)
    ssh = SSHKeyAuth(entry)

    #GNS3 Project VM
    ssh.tryAuth("192.168.122.185", "root", timeSafety=5)
    telNetNoPassword = telnet.tryAuth(host, timeSafety=5)
    if(telNetNoPassword):
        validateLastLine(entry, expectedLastLine)

    entry.spawnNewShell()
    #GNS3 Project VM
    ssh.tryAuth("192.168.122.185", "root", timeSafety=5)

    telNetPasswordOnly = telnet.tryAuth(host, password="Password1", timeSafety=5)
    if(telNetPasswordOnly):
        validateLastLine(entry, expectedLastLine)

    entry.spawnNewShell()
    #GNS3 Project VM
    ssh.tryAuth("192.168.122.185", "root", timeSafety=5)

    telNetUserPassword = telnet.tryAuth(host, user="User", password="Password1", timeSafety=5)
    if(telNetUserPassword):
        validateLastLine(entry, expectedLastLine)

    entry.spawnNewShell()
    #GNS3 Project VM
    ssh.tryAuth("192.168.122.185", "root", timeSafety=5)

    #technically it can handle user@host assuming keys are done correctly it's fine
    SSHKey = ssh.tryAuth(host, timeSafety=5)
    if(SSHKey):
        validateLastLine(entry, expectedLastLine)

    entry.spawnNewShell()
    #GNS3 Project VM
    ssh.tryAuth("192.168.122.185", "root", timeSafety=5)

    SSHUserPassword = ssh.tryAuth(host, user="User", password="Password1", timeSafety=5)
    if(SSHUserPassword):
        validateLastLine(entry, expectedLastLine)

    return telNetNoPassword, telNetPasswordOnly, telNetUserPassword, SSHKey, SSHUserPassword


def worker(testCases: tuple[bool], host: str, expectedLastLine: str):
    a = JumpHost("10.21.37.2", "root", keyPath="C:/Users/Mateusz/.ssh/id_ed25519")
    result = theoreticallyAllCases(a, host, expectedLastLine)
    if(testCases != result):
        print(f"{host} failed testing tests -> " + str(result))
    else:
        print(f"{host} passed tests")


if __name__=="__main__":
    start = time.time()

    host02 = threading.Thread(target=worker, args=((True, True, True, False, False), "10.0.0.2", "TelnetNoPassword>"))
    host02.start()

    host03 = threading.Thread(target=worker, args=((False, True, True, False, False), "10.0.0.3", "TelnetOnlyPassword>"))
    host03.start()

    host04 = threading.Thread(target=worker, args=((False, False, True, False, False), "10.0.0.4", "TelnetUserPassword>"))
    host04.start()

    #Expected behaviour of last test
    host05 = threading.Thread(target=worker, args=((False, False, False, True, True), "10.0.0.5", "SSHKey>"))
    host05.start()

    host06 = threading.Thread(target=worker, args=((False, False, False, False, True), "10.0.0.6", "SSHUserPassword>"))
    host06.start()

    #120 seems good to test all auth slow but w/e
    host02.join(120)
    host03.join(120)
    host04.join(120)
    host05.join(120)
    host06.join(120)

    finish = time.time()
    difference = int(finish - start)
    #On my machine 97 seconds, so to try all auth types with timeout 5 is around 80 seconds assuming only one host
    print("Tests took time to run in seconds: " + str(difference))