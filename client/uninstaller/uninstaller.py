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
        pass

    def windows_remove(self):
        subprocess.call("nssm.exe remove harvester")


if __name__ == "main":
    setup = Setup()
