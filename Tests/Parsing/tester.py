import logging

from wrapper.Vendor.Cisco_IOS import Cisco_IOS

if __name__ == "__main__":
    logging.getLogger("paramiko").setLevel(logging.DEBUG)
    a = Cisco_IOS("10.21.37.204", "root", ssh_key_path="C:/Users/Mateusz/Desktop/id_rsa")
    print(a.getInterfaces())
    print(a.interfaceDescriptions)
    print(a.interfaceStatus)