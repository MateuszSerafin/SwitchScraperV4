class EntryPoint:

    def readAll(self, timeout = 20) -> list[bytes]:
        raise Exception("This is interface")

    def write(self, command: bytes):
        raise Exception("This is interface")

    def spawnNewShell(self) -> Exception:
        raise Exception("This is interface")

