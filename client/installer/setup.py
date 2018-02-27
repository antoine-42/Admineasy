import platform
import subprocess
import ctypes
import sys
import os


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
        dir_path = os.getcwd()
        app_path = dir_path.split("harvester-setup")[0]
        if not Setup.windows_is_admin():
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, "", None, 1)
            sys.exit()
        subprocess.call("nssm.exe install harvester '" + app_path + "\harvester\harvester.exe'")
        subprocess.call("nssm.exe set harvester Description \"Admineasy client.\"")
        subprocess.call("nssm.exe set harvester Start SERVICE_AUTO_START")
        subprocess.call("nssm.exe set harvester AppStdout \"C:\logs\harvester-log.log\"")
        subprocess.call("nssm.exe start harvester")

    @staticmethod
    def windows_is_admin():
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False


if __name__ == "__main__":
    setup = Setup()
