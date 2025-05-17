# SwitchScraperV4

## Tldr
1. I needed to dump information from switches (Port Descriptions, Vlans, Status etc.)
2. Previously I didn't know about netmiko and ntc-templates
3. I don't need it at the moment
4. Getting Virtual images to test this on GNS3 is real problem hence only Cisco implementation as of now
5. Current code is good, adding support to other vendors should be really easy

## Sample Usage
```python
from wrapper.Vendor.Cisco_IOS import Cisco_IOS
switch = Cisco_IOS("10.21.37.201", "User", "Password1")
interfaces = switch.getInterfaces()
#['GigabitEthernet0/0', 'GigabitEthernet0/1', 'GigabitEthernet0/2', 'GigabitEthernet0/3', 'GigabitEthernet1/0', 'GigabitEthernet1/1', 'GigabitEthernet1/2', 'GigabitEthernet1/3', 'GigabitEthernet2/0', 'GigabitEthernet2/1', 'GigabitEthernet2/2', 'GigabitEthernet2/3', 'GigabitEthernet3/0', 'GigabitEthernet3/1', 'GigabitEthernet3/2', 'GigabitEthernet3/3', 'Vlan2137']
print(interfaces)
#1
print(switch.getUntaggedOnPort(interfaces[1]))
#{1: 'default', 2: 'iksde', 1002: 'fddi-default', 1003: 'token-ring-default', 1004: 'fddinet-default', 1005: 'trnet-default', 2137: 'VLAN2137'}
print(switch.getVlansWithDescription())
```