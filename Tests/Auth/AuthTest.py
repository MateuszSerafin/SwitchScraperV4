from wrapper.Vendor.Cisco_IOS import Cisco_IOS
import time

#10.21.37.201 -> TelnetNoPassword
#10.21.37.202 -> TelnetOnlyPassword
#10.21.37.203 -> TelnetUserPassword
#10.21.37.204 -> SSHKey
#10.21.37.205 -> SSHUserPassword
#All switches have the same users and password (User, Password1)

def testThisIpCisco(ip: str, expectedLastLine: str, user="User", password="Password1", key_path="C:/Users/Mateusz/Desktop/id_rsa") -> bool:
    return expectedLastLine == Cisco_IOS(ip, user, password, key_path).conn.find_prompt()


if __name__ == "__main__":
    start = time.time()
    print(testThisIpCisco("10.21.37.201", "TelnetNoPassword>"))
    print(testThisIpCisco("10.21.37.202", "TelnetOnlyPassword>"))
    print(testThisIpCisco("10.21.37.203", "TelnetUserPassword>"))
    print(testThisIpCisco("10.21.37.204", "SSHKey>", user="root"))
    print(testThisIpCisco("10.21.37.205", "SSHUserPassword>"))
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