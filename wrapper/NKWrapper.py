import logging
from os import path
from netmiko import BaseConnection, ConnectHandler

#Without it errors gets print to console even i am catching it.
logging.getLogger('paramiko.transport').addHandler(logging.NullHandler())

class NKWrapper:

    device_type: str
    conn: BaseConnection

    # TODO change it so there is options to disable ssh, telnet no password etc. For me this is good enough
    # disabled_algorithms should be better documented or implemented more correctly the tldr is old switches suppoer rsa-rsa or something like that but by default not tried.
    def __init__(self, ip: str, device_type: str, username: str = None, password: str = None, ssh_key_path: path = None, ssh_disabled_algorithms=dict(pubkeys=["rsa-sha2-512", "rsa-sha2-256"])):
        super().__init__()
        self.device_type = device_type

        authToTry = []

        if (username != None and password != None):
            authToTry.append({"host": ip, "device_type": device_type, "password": password, "username": username, "disabled_algorithms": ssh_disabled_algorithms})

        if(ssh_key_path is not None):
            if(username is None):
                raise Exception("Username is required while providing key auth")
            authToTry.append({"host": ip, "device_type": device_type, "username": username, "use_keys": True, "key_file": ssh_key_path, "disabled_algorithms": ssh_disabled_algorithms})

        # There are 3 auth types nopassword, password only and user password
        # when provided username, password it won't auth against no password
        # when provided password it won't auth against username and password
        # hence it requires 3 separate login attempts
        authToTry.append({"host": ip, "device_type": device_type + "_telnet"})

        if (password != None):
            authToTry.append({"host": ip, "device_type": device_type + "_telnet", "password": password})
            if (username != None):
                authToTry.append({"host": ip, "device_type": device_type + "_telnet", "password": password, "username": username})

        # Past this point technically all the auth types should be build
        for auth in authToTry:
            try:
                self.conn = ConnectHandler(**auth)
                return
            except Exception as e:
                continue
        raise Exception("Failed to authenticate")

    # All of it should be safe to call because we raise if auth fails
    def getDeviceType(self) -> str:
        return self.device_type

    def executeCommand(self, command: str) -> str:
        return self.conn.send_command(command)

    def closeConnection(self):
        self.conn.disconnect()