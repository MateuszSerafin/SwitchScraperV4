from wrapper import Helpers
from wrapper.SwitchData import SwitchData

def switchDataToCSV(switchData: SwitchData):
    csvString = "VLANs\nVlanID,Description\n"

    for vlan, description in switchData.getVlansWithDescription().items():
        csvString += f"{vlan},{description}\n"

    csvString += "\nInterfaces\nInterface Name,Status,IP Address, Untagged, Tagged, Description\n"

    for interface in switchData.getInterfaces():
        ipAddress = switchData.getInterfaceIpAddress(interface)
        if(ipAddress == None):
            ipAddress = "Not assigned"

        untagged = switchData.getUntaggedOnPort(interface)
        if(untagged == None):
            untagged = "None untagged"

        tagged = switchData.getTaggedVlansOnPort(interface)
        if(tagged == None):
            tagged = "None"
        else:
            tagged = Helpers.collapse_ranges(tagged).replace(",", ";")
        csvString += f"{interface},{switchData.getInterfaceStatus(interface)},{ipAddress},{untagged},{tagged},{switchData.getInterfaceDescription(interface)}\n"

    csvString += "\nLAG Interfaces\nInterface Name,Members\n"
    for lagInterface, members in switchData.getChannelPortsAndMembers().items():
        membersAsString = ""
        for member in members:
            membersAsString += member + ","


        csvString += f"{lagInterface},{membersAsString}\n"

    csvString += "\nMAC Address Table\nInterface Name,MAC Addresses\n"
    for interface in switchData.getInterfaces():
        macString = ""
        macAddresses = switchData.macAddressesOnInterface(interface)
        if(macAddresses == None):
            macString = "No devices"
        else:
            for macAddress in macAddresses:
                macString += macAddress + ","
        csvString += f"{interface}, {macString}\n"

    csvString += "\nLLDP Info\nLocal Interface,MGMT Address,Mac Address, Remote Interface,System Name,System Description\n"

    for interface in switchData.getInterfaces():
        lldpNeigboursOnInterface = switchData.getLLDPOnInterface(interface)
        #Let's skip interfaces where there is no neighbours
        if(lldpNeigboursOnInterface == None):
            continue
        for neigbour in lldpNeigboursOnInterface:
            csvString += f"{interface},{neigbour.getMgmtAddress()},{neigbour.getMacAddress()},{neigbour.getRemoteInterface()},{neigbour.getSystemName()},{neigbour.getSystemDescription().replace(",", ";")}\n"

    csvString += "\n\nDumped using SwitchScraperV4"
    return csvString