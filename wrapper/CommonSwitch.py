import json

class CommonSwitch:

    interfaces: list[str]
    interfaceStatus: dict[str, str]
    interfaceDescriptions: dict[str, str]

    vlansDescriptions: dict[int, str]
    vlansTagged: dict[str, list[int]]
    vlansUntagged: dict[str, int]


    def __init__(self):
        super().__init__()
        self.interfaces = []
        self.interfaceStatus = {}
        self.interfaceDescriptions = {}

        self.vlansDescriptions = {}
        self.vlansTagged = {}
        self.vlansUntagged = {}


    @staticmethod
    def fromJson(jsondata: str):
        Instance = CommonSwitch()
        saved = json.loads(jsondata)
        Instance.interfaces = saved["interfaces"]
        Instance.interfaceStatus = saved["interfaceStatus"]
        Instance.interfaceDescriptions = saved["interfaceDescriptions"]
        Instance.vlansTagged = saved["vlansTagged"]
        Instance.vlansUntagged = saved["vlansUntagged"]

        return Instance

    def dumpToJson(self) -> str:
        return json.dumps({"interfaces": self.interfaces,
                           "interfaceStatus": self.interfaceStatus,
                           "interfaceDescriptions": self.interfaceDescriptions,
                           "vlansTagged": self.vlansTagged,
                           "vlansUntagged": self.vlansUntagged})

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

    def getVlansWithDescription(self) -> dict[int, str]:
        return self.vlansDescriptions

    def getTaggedVlansOnPort(self, interface: str) -> list[int] | None:
        return self.vlansTagged[interface]

    # If trunk port or layer 3 port i will try to follow that for other vendors
    def getUntaggedOnPort(self, interface: str) -> int | None:
        return self.vlansUntagged[interface]