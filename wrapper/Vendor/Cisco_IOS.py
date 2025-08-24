from os import path
from wrapper import Helpers
from wrapper.NKWrapper import NKWrapper
from ntc_templates.parse import parse_output
from wrapper.SwitchData import SwitchData, LldpInfo

class Cisco_IOS(NKWrapper):

    _switchData: SwitchData
    #If no trunks it would constantly fire,  N/A to other commands as there is way to check if they were executed
    _didRunShowTrunk: bool
    _didRunPortChannelInfo: bool
    _didRunLLDPInfo: bool

    def __init__(self, ip: str, username: str = None, password: str = None, ssh_key_path: path = None, ssh_disabled_algorithms=dict(pubkeys=["rsa-sha2-512", "rsa-sha2-256"])):
        super().__init__(ip, "cisco_ios", username, password, ssh_key_path, ssh_disabled_algorithms=ssh_disabled_algorithms)
        self._didRunShowTrunk = False
        self._didRunPortChannelInfo = False
        self._didRunLLDPInfo = False
        self._switchData = SwitchData()

    def getSwitchData(self) -> SwitchData:
        return self._switchData

    def _collectInterfaces(self) -> None:
        raw = self.executeCommand("show interfaces description")
        parsed = parse_output(platform=self.device_type, command="show interfaces description", data=raw)
        for port in parsed:
            # It returns Gi instead of full interface name
            portName = Helpers.convertShortIntName(port["port"])
            portStatus = port["status"]
            portDescription = port["description"]
            self._switchData._interfaces.append(portName)
            self._switchData._interfaceStatus[portName] = portStatus
            self._switchData._interfaceDescriptions[portName] = portDescription

    def _collectInterfaceIpAddresses(self) -> None:
        raw = self.executeCommand("show ip interface brief")
        parsed = parse_output(platform=self.device_type, command="show ip interface brief", data=raw)
        for toCheck in parsed:
            interfaceName = toCheck["interface"]
            shouldContainIP = toCheck["ip_address"]
            if (Helpers.isStringIpAddress(shouldContainIP)):
                self._switchData._interfaceIpAddresses[interfaceName] = shouldContainIP

    def _collectVlansWithDescriptions(self) -> None:
        raw = self.executeCommand("show vlan")
        parsed = parse_output(platform=self.device_type, command="show vlan", data=raw)
        for vlan in parsed:
            vlanID = int(vlan["vlan_id"])
            vlanName = vlan["vlan_name"]
            for interface in vlan["interfaces"]:
                self._switchData._vlansUntagged[Helpers.convertShortIntName(interface)] = vlanID
            self._switchData._vlansDescriptions[vlanID] = vlanName

    def _collectTrunkInformation(self) -> None:
        raw = self.executeCommand("show int trunk").split("\n")
        # no trunks configured
        if (raw == ['']):
            self._didRunShowTrunk = True
            return None

        processIndex = None

        for line in raw:
            if ("Vlans allowed on trunk" in line):
                processIndex = raw.index(line)
                break
        if (processIndex == None):
            raise Exception("Failed to parse show int trunk command")

        for line in raw[processIndex + 1:]:
            if ("Port" in line or line == ""):
                break
            splited = line.split(" ")
            inter = Helpers.convertShortIntName(splited[0])
            vlans = Helpers.expand_ranges(splited[-1])
            self._switchData._vlansTagged[inter] = vlans
        self._didRunShowTrunk = True

    def _collectPortChannelMembers(self) -> None:
        raw = self.executeCommand("show etherchannel summary")
        parsed = parse_output(platform=self.device_type, command="show etherchannel summary", data=raw)
        for bundle in parsed:
            portChannelName = Helpers.convertShortIntName(bundle["bundle_name"])
            members = [Helpers.convertShortIntName(x) for x in bundle["member_interface"]]
            if (portChannelName not in self._switchData._channelPorts):
                self._switchData._channelPorts[portChannelName] = members
                continue
            raise Exception("This should not happen")
        self._didRunPortChannelInfo = True

    def _collectMacAddressTable(self) -> None:
        raw = self.executeCommand("show mac address-table")
        parsed = parse_output(platform=self.device_type, command="show mac address-table", data=raw)
        for toIter in parsed:
            mac = toIter["destination_address"]
            port = toIter["destination_port"]

            if (len(port) != 1):
                raise Exception("I don't know when this happens it requires further testing")

            port = Helpers.convertShortIntName(port[0])

            if (port not in self._switchData._macAddresses):
                self._switchData._macAddresses[port] = [mac]
                continue
            self._switchData._macAddresses[port].append(mac)

    def _collectLLDPInfo(self) -> None:
        raw = self.executeCommand("show lldp neighbors detail")
        parsed = parse_output(platform=self.device_type, command="show lldp neighbors detail", data=raw)
        for lldpNeigbour in parsed:
            localInterface = Helpers.convertShortIntName(lldpNeigbour["local_interface"])

            mgmtAddress = lldpNeigbour["mgmt_address"]
            macAddress = lldpNeigbour["chassis_id"]
            # TODO this should check chass_id and mac_address and check which one is actual mac-address
            remoteInterface = Helpers.convertShortIntName(lldpNeigbour["neighbor_interface"])
            neighbourName = lldpNeigbour["neighbor_name"]
            neighbourDescription = lldpNeigbour["neighbor_description"]

            lldpInfoInstance = LldpInfo(mgmtAddress, macAddress, remoteInterface, neighbourName, neighbourDescription)

            if (localInterface not in self._switchData._lldpInfo):
                self._switchData._lldpInfo[localInterface] = [lldpInfoInstance]
                continue

            self._switchData._lldpInfo[localInterface].append(lldpInfoInstance)

    def getInterfaces(self) -> list[str]:
        if(len(self._switchData._interfaces) == 0):
            self._collectInterfaces()
            return self._switchData.getInterfaces()
        else:
            return self._switchData.getInterfaces()

    def getInterfaceStatus(self, interface: str) -> str:
        if(len(self._switchData._interfaceStatus) == 0):
            self.getInterfaces()
        return self._switchData.getInterfaceStatus(interface)

    def getInterfaceDescription(self, interface: str) -> str:
        if(len(self._switchData._interfaceDescriptions) == 0):
            self.getInterfaces()
        return self._switchData.getInterfaceDescription(interface)

    def getInterfaceIpAddress(self, interface: str) -> str | None:
        if(len(self._switchData._interfaceIpAddresses) == 0):
            self._collectInterfaceIpAddresses()
        return self._switchData.getInterfaceIpAddress(interface)

    def getVlansWithDescription(self) -> dict[int, str]:
        if(len(self._switchData._vlansDescriptions) == 0):
            self._collectVlansWithDescriptions()
        return self._switchData.getVlansWithDescription()

    def getTaggedVlansOnPort(self, interface: str) -> list[int] | None:
        # there is no ntc parser for that
        if(not self._didRunShowTrunk):
            self._collectTrunkInformation()
        return self._switchData.getTaggedVlansOnPort(interface)

    def getUntaggedOnPort(self, interface: str) -> int | None:
        # show vlan shows untagged information any way make it depend on it
        if(len(self._switchData._vlansDescriptions) == 0):
            self.getVlansWithDescription()
        if(interface not in self._switchData._vlansUntagged):
            return None
        return self._switchData._vlansUntagged[interface]

    def getChannelPortsAndMembers(self) -> dict[str, list[str]]:
        if(not self._didRunPortChannelInfo):
            self._collectPortChannelMembers()
        return self._switchData.getChannelPortsAndMembers()

    def getPortChannelName(self, interface: str) -> str | None:
        self.getChannelPortsAndMembers()
        return self._switchData.getPortChannelName(interface)

    def macAddressesOnInterface(self, interface: str) -> list[str] | None:
        if(len(self._switchData._macAddresses) == 0):
            self._collectMacAddressTable()
        return self._switchData.macAddressesOnInterface(interface)

    def getLLDPOnInterface(self, interface: str) -> list[LldpInfo] | None:
        if(not self._didRunLLDPInfo):
            self._collectLLDPInfo()
        return self._switchData.getLLDPOnInterface(interface)

    def collectAll(self) -> None:
        self._collectInterfaces()
        self._collectInterfaceIpAddresses()
        self._collectVlansWithDescriptions()
        self._collectTrunkInformation()
        self._collectPortChannelMembers()
        self._collectMacAddressTable()
        self._collectLLDPInfo()