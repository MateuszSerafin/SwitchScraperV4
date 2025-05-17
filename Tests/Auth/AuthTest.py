from typing import Type
from wrapper.NKWrapper import NKWrapper
from wrapper.Vendor.Cisco_IOS import Cisco_IOS
import time

def crapWrap(ip: str, expectedLastLine: str, wrapper: Type[NKWrapper],  user="User", password="Password1", key_path="/home/mateusz/Downloads/id_rsa") -> str:
    if(wrapper == Cisco_IOS):
        return f"{expectedLastLine}:{expectedLastLine == Cisco_IOS(ip, user, password, key_path).conn.find_prompt()}"
    raise Exception("Not implemented")

def ciscoTest():
    print(crapWrap("10.21.37.201", "CiscoTelnetNoPassword>", Cisco_IOS))
    print(crapWrap("10.21.37.202", "CiscoTelnetOnlyPassword>", Cisco_IOS))
    print(crapWrap("10.21.37.203", "CiscoTelnetUserPassword>", Cisco_IOS))
    print(crapWrap("10.21.37.204", "CiscoSSHKey>", Cisco_IOS, user="root"))
    print(crapWrap("10.21.37.205", "CiscoSSHUserPassword>", Cisco_IOS))

if __name__ == "__main__":
    start = time.time()
    ciscoTest()
    end = time.time()
    print("Time to run: " +  str(end - start))
    '''
    True
    True
    True
    True
    True
    Time to run: 31.466190814971924
    Good enough
    '''