import json

class LldpInfo:

    _mgmtAddress: str
    _macAddress: str
    _remoteInterface: str
    _systemName: str
    _systemDescription: str

    def __init__(self, mgmtAddress: str = "", macAddress: str = "", remoteInterface: str = "", systemName: str = "", systemDescription: str= ""):
        self._mgmtAddress = mgmtAddress
        self._macAddress = macAddress
        self._remoteInterface = remoteInterface
        self._systemName = systemName
        self._systemDescription = systemDescription

    def getMgmtAddress(self) -> str:
        return self._mgmtAddress

    def getMacAddress(self) -> str:
        return self._macAddress

    def getRemoteInterface(self) -> str:
        return self._remoteInterface

    def getSystemName(self) -> str:
        return self._systemName

    def getSystemDescription(self) -> str:
        return self._systemDescription

class SwitchData:

    _interfaces: list[str]
    _interfaceStatus: dict[str, str]
    _interfaceDescriptions: dict[str, str]
    _interfaceIpAddresses: dict[str, str]

    _vlansDescriptions: dict[int, str]
    _vlansTagged: dict[str, list[int]]
    _vlansUntagged: dict[str, int]

    _channelPorts: dict[str, list[str]]
    _macAddresses: dict[str, list[str]]
    _lldpInfo: dict[str, list[LldpInfo]]

    def __init__(self):
        super().__init__()
        self._interfaces = []
        self._interfaceStatus = {}
        self._interfaceDescriptions = {}
        self._interfaceIpAddresses = {}

        self._vlansDescriptions = {}
        self._vlansTagged = {}
        self._vlansUntagged = {}

        self._channelPorts = {}
        self._macAddresses = {}
        self._lldpInfo = {}

    @staticmethod
    def fromJson(data: str) -> 'SwitchData':
        switchDataInstance = SwitchData()
        rawData = json.loads(data)
        lldpInfoRaw = rawData["_lldpInfo"]
        del rawData["_lldpInfo"]
        switchDataInstance.__dict__.update(rawData)
        for interface, lldpInfoList in lldpInfoRaw.items():
            for lldpInfo in lldpInfoList:
                lldpInstance = LldpInfo()
                lldpInstance.__dict__.update(lldpInfo)
                if(interface not in switchDataInstance._lldpInfo):
                    switchDataInstance._lldpInfo[interface] = [lldpInstance]
                    continue
                switchDataInstance._lldpInfo[interface].append(lldpInstance)
        return switchDataInstance

    def toJson(self) -> str:
        return json.dumps(self, default=vars)

    def getInterfaces(self) -> list[str]:
        return self._interfaces

    def getInterfaceStatus(self, interface: str) -> str | None:
        if(interface in self._interfaceStatus):
            return self._interfaceStatus[interface]
        else:
            return None

    def getInterfaceDescription(self, interface: str) -> str | None:
        if(interface in self._interfaceDescriptions):
            return self._interfaceDescriptions[interface]
        else:
            return None

    def getInterfaceIpAddress(self, interface: str) -> str | None:
        if(interface in self._interfaceIpAddresses):
            return self._interfaceIpAddresses[interface]
        return None

    def getVlansWithDescription(self) -> dict[int, str]:
        return self._vlansDescriptions

    def getTaggedVlansOnPort(self, interface: str) -> list[int] | None:
        if(interface in self._vlansTagged):
            return self._vlansTagged[interface]
        return None

    def getUntaggedOnPort(self, interface: str) -> int | None:
        if(interface in self._vlansUntagged):
            return self._vlansUntagged[interface]
        return None

    def getChannelPortsAndMembers(self) -> dict[str, list[str]]:
        return self._channelPorts

    def getPortChannelName(self, interface: str) -> str | None:
        for key, value in self._channelPorts.items():
            for toCheck in value:
                if(interface == toCheck):
                    return key
        return None

    def macAddressesOnInterface(self, interface: str) -> list[str] | None:
        if(interface in self._macAddresses):
            return self._macAddresses[interface]
        return None

    def getLLDPOnInterface(self, interface: str) -> list[LldpInfo] | None:
        if(interface in self._lldpInfo):
            return self._lldpInfo[interface]
        return None