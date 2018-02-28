import platform
import subprocess


class Setup:
    def __init__(self):
        self.os = platform.system()
        if self.os == "Linux":
            self.linux_remove()
        elif self.os == "Windows":
            self.windows_remove()

    def linux_remove(self):
        subprocess.call(["/usr/bin/sudo", "systemctl", "stop", "admineasy-harvester.service"])
        subprocess.call(["/usr/bin/sudo", "systemctl", "disable", "admineasy-harvester.service"])
        subprocess.call(["/usr/bin/sudo", "rm", "/etc/systemd/system/admineasy-harvester.service"])
        subprocess.call(["/usr/bin/sudo", "systemctl", "daemon-reload"])

    def windows_remove(self):
        subprocess.call(["nssm.exe", "stop", "harvester"])
        subprocess.call(["nssm.exe", "remove", "harvester", "confirm"])


if __name__ == "__main__":
    setup = Setup()
