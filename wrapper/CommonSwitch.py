class CommonSwitch:

    interfaces: list[str]
    interfaceStatus: dict[str, str]
    interfaceDescriptions: dict[str, str]

    def __init__(self):
        super().__init__()
        self.interfaces = []
        self.interfaceStatus = {}
        self.interfaceDescriptions = {}

    def getInterfaces(self) -> list[str]:
        return self.interfaces

    def getInterfaceStatus(self, interface: str) -> str | None:
        if(interface in self.interfaceStatus):
            return self.interfaceStatus[interface]
        else:
            return None

    def getInterfaceDescription(self, interface: str) -> str | None:
        if(interface in self.interfaceDescriptions):
            return self.interfaceDescriptions[interface]
        else:
            return None