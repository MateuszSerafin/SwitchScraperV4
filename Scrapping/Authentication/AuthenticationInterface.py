class AuthenticationInterface:

    def tryAuth(self, ip: str, user: str = None, password: str = None, timeSafety:int = 20, consoleDetection = [">", "#"], options: str="") -> bool:
        raise Exception("This is interface")