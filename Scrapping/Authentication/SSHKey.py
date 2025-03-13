from Scrapping.Authentication.AuthenticationInterface import AuthenticationInterface
from Scrapping.EntryPoints.EntryPointInterface import EntryPoint

class SSHKeyAuth(AuthenticationInterface):

    entryPointInterface: EntryPoint

    def __init__(self, entryPointInterface: EntryPoint):
        self.entryPointInterface = entryPointInterface

    def tryAuth(self, ip: str, user: str = None, password: str = None, timeSafety: int = 20, consoleDetection = [">", "#"], options: str="") -> bool:
        self.entryPointInterface.write(b"\n")
        currentSession = self.entryPointInterface.readAll(2)
        localMachineDetection = ""
        for cns in consoleDetection:
            for line in currentSession:
                line = str(line)
                if(cns in line):
                    localMachineDetection = str(line).replace("\n", "").replace("\r", "").replace("\\r", "")

        if(user != None):
            self.entryPointInterface.write(bytes(f"ssh {user}@{ip} {options}\n", "utf-8"))
        else:
            self.entryPointInterface.write(bytes(f"ssh {ip} {options}\n", "utf-8"))

        okaySoNow_What = self.entryPointInterface.readAll(timeSafety)
        LastLine = str(okaySoNow_What[len(okaySoNow_What) - 1])
        if("password:" in LastLine.lower()):
            if(password == None):
                return False
            else:
                self.entryPointInterface.write(bytes(f"{password}\n", "utf-8"))
                iAmLastLineNow = self.entryPointInterface.readAll(timeSafety)
                if("password:" in str(iAmLastLineNow[len(iAmLastLineNow) - 1]).lower()):
                    return False
                LastLine = str(iAmLastLineNow[len(iAmLastLineNow) - 1]).lower()

        for cns in consoleDetection:
            if(cns in LastLine):
                if(localMachineDetection in LastLine):
                    return False
                return True
        return False