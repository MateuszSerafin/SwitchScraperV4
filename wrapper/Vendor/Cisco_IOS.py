from os import path
from wrapper.CommonSwitch import CommonSwitch
from wrapper.NKWrapper import NKWrapper
from ntc_templates.parse import parse_output

class Cisco_IOS(NKWrapper, CommonSwitch):

    #If no trunks it would constantly fire,  N/A to other commands as there is way to check if they were executed
    didRunShowTrunk: bool

    def __init__(self, ip: str, username: str = None, password: str = None, ssh_key_path: path = None, ssh_disabled_algorithms=dict(pubkeys=["rsa-sha2-512", "rsa-sha2-256"])):
        super().__init__(ip, "cisco_ios", username, password, ssh_key_path, ssh_disabled_algorithms=ssh_disabled_algorithms)

        self.didRunShowTrunk = False

    def getInterfaces(self) -> list[str]:
        if(len(self.interfaces) == 0):
            raw = self.executeCommand("show interfaces description")
            parsed = parse_output(platform=self.device_type, command="show interfaces description", data=raw)
            for port in parsed:
                #It returns Gi instead of full interface name
                portName = _convertShortIntName(port["port"])
                portStatus = port["status"]
                portDescription = port["description"]
                self.interfaces.append(portName)
                self.interfaceStatus[portName] = portStatus
                self.interfaceDescriptions[portName] = portDescription
            return self.interfaces
        else:
            return self.interfaces

    def getInterfaceStatus(self, interface: str) -> str:
        if(len(self.interfaceStatus) == 0):
            self.getInterfaces()
        return self.interfaceStatus[interface]

    def getInterfaceDescription(self, interface: str) -> str:
        if(len(self.interfaceDescriptions) == 0):
            self.getInterfaces()
        return self.interfaceDescriptions[interface]

    def getVlansWithDescription(self) -> dict[int, str]:
        if(len(self.vlansDescriptions) == 0):
            raw = self.executeCommand("show vlan")
            parsed = parse_output(platform=self.device_type, command="show vlan", data=raw)
            for vlan in parsed:
                vlanID = int(vlan["vlan_id"])
                vlanName = vlan["vlan_name"]
                for interface in vlan["interfaces"]:
                    self.vlansUntagged[_convertShortIntName(interface)] = vlanID
                self.vlansDescriptions[vlanID] = vlanName
        return self.vlansDescriptions

    def getTaggedVlansOnPort(self, interface: str) -> list[int] | None:
        # there is no ntc parser for that
        if(not self.didRunShowTrunk):
            raw = self.executeCommand("show int trunk").split("\n")
            # no trunks configured
            if(raw == ['']):
                self.didRunShowTrunk =  True
                return None

            processIndex = None

            for line in raw:
                if("Vlans allowed on trunk" in line):
                    processIndex = raw.index(line)
                    break
            if(processIndex == None):
                raise Exception("Failed to parse show int trunk command")

            for line in raw[processIndex + 1:]:
                if("Port" in line or line == ""):
                    break
                splited = line.split(" ")
                inter = _convertShortIntName(splited[0])
                vlans = _expand_ranges(splited[-1])
                self.vlansTagged[inter] = vlans
            self.didRunShowTrunk = True
        if(interface not in self.vlansTagged):
            return None
        return self.vlansTagged[interface]


    def getUntaggedOnPort(self, interface: str) -> int | None:
        # show vlan shows untagged information any way make it depend on it
        if(len(self.vlansDescriptions) == 0):
            self.getVlansWithDescription()
        if(interface not in self.vlansUntagged):
            return None
        return self.vlansUntagged[interface]

# Helpers
def _expand_ranges(range_str):
    numbers = []
    for part in range_str.split(','):
        if '-' in part:
            start, end = map(int, part.split('-'))
            numbers.extend(range(start, end + 1))
        else:
            numbers.append(int(part))
    return numbers

_theremightbemore = {
    "Gi": "GigabitEthernet",
    "Fa": "FastEthernet",
    "Te": "TenGigabitEthernet",
    "Vl": "Vlan"
}

def _convertShortIntName(shouldBeShort: str) -> str:
    for key, value in _theremightbemore.items():
        if(key in shouldBeShort and value not in shouldBeShort):
            return shouldBeShort.replace(key, value)
    return shouldBeShort