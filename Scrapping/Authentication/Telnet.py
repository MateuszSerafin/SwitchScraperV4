from Scrapping.Authentication.AuthenticationInterface import AuthenticationInterface
from Scrapping.EntryPoints.EntryPointInterface import EntryPoint

class Telnet(AuthenticationInterface):

    entryPointInterface: EntryPoint

    def __init__(self, entryPointInterface: EntryPoint):
        self.entryPointInterface = entryPointInterface

    def tryAuth(self, ip: str, user: str = None, password: str = None, timeSafety:int = 20, consoleDetection = [">", "#"], options: str="") -> bool:
        self.entryPointInterface.write(b"\n")
        currentSession = self.entryPointInterface.readAll(2)
        localMachineDetection = ""
        for cns in consoleDetection:
            for line in currentSession:
                line = str(line)
                if(cns in line):
                    localMachineDetection = str(line).replace("\n", "").replace("\r", "").replace("\\r", "")

        self.entryPointInterface.write(bytes(f"telnet {ip} {options}\n", "utf-8"))

        while True:
            okaySoNow_What = self.entryPointInterface.readAll(timeSafety)
            LastLine = str(okaySoNow_What[len(okaySoNow_What) - 1])

            #First check for no auth
            for cns in consoleDetection:
                if (cns in LastLine):
                    if (localMachineDetection in LastLine):
                        return False
                    return True
            #Replace other crap

            if("password:" in LastLine.lower()):
                if(password == None):
                    return False
                else:
                    self.entryPointInterface.write(bytes(f"{password}\n", "utf-8"))
                    continue

            userMatches = ["user", "login", "username"]
            con = False
            for usrmatch in userMatches:
                if(usrmatch in LastLine.lower()):
                    if(user == None):
                        return False
                    else:
                        self.entryPointInterface.write(bytes(f"{user}\n", "utf-8"))
                        con = True
                        break
            if(con):
                continue
            return False







