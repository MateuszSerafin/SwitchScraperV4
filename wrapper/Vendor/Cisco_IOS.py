from os import path
from wrapper.CommonSwitch import CommonSwitch
from wrapper.NKWrapper import NKWrapper
from ntc_templates.parse import parse_output

class Cisco_IOS(NKWrapper, CommonSwitch):

    def __init__(self, ip: str, username: str = None, password: str = None, ssh_key_path: path = None, ssh_disabled_algorithms=dict(pubkeys=["rsa-sha2-512", "rsa-sha2-256"])):
        super().__init__(ip, "cisco_ios", username, password, ssh_key_path, ssh_disabled_algorithms=ssh_disabled_algorithms)

    def getInterfaces(self) -> list[str]:
        if(len(self.interfaces) == 0):
            raw = self.executeCommand("show interfaces description")
            parsed = parse_output(platform=self.device_type, command="show interfaces description", data=raw)
            for port in parsed:
                portName = port["port"]
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


