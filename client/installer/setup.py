import platform
import subprocess


class Setup:
    def __init__(self):
        self.os = platform.system()
        if self.os == "Linux":
            self.linux_setup()
        elif self.os == "Windows":
            self.windows_setup()

    def linux_setup(self):
        pass

    def windows_setup(self):
        subprocess.call("nssm.exe install harvester harvester.exe")
        subprocess.call("nssm.exe set harvester Description \"Admineasy client.\"")
        subprocess.call("nssm.exe set harvester Start SERVICE_AUTO_START")
        subprocess.call("nssm.exe set harvester AppStdout \"C:\logs\harvester-log.log\"")
        subprocess.call("nssm.exe start harvester")


if __name__ == "main":
    setup = Setup()
