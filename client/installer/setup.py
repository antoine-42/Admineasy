import platform
import subprocess
import ctypes
import sys
import os
import time


class Setup:
    def __init__(self):
        self.os = platform.system()
        if self.os == "Linux":
            self.linux_setup()
        elif self.os == "Windows":
            self.windows_setup()

    def linux_setup(self):
        subprocess.call(["/usr/bin/sudo", "mv", "admineasy-harvester.service", "/etc/systemd/system/"])
        subprocess.call(["/usr/bin/sudo", "systemctl", "enable", "admineasy-harvester.service"])
        subprocess.call(["/usr/bin/sudo", "systemctl", "start", "admineasy-harvester.service"])

    def windows_setup(self):
        # get path to application
        dir_path = os.getcwd()
        app_path = dir_path.split("harvester-setup")[0] + "\\harvester\\harvester.exe"
        # get admin privileges
        if not Setup.windows_is_admin():
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, "", None, 1)
        # setup service
        subprocess.call(["nssm.exe", "install", "harvester", app_path])
        subprocess.call(["nssm.exe", "set", "harvester", "Description", "Admineasy client."])
        subprocess.call(["nssm.exe", "set", "harvester", "Start", "SERVICE_AUTO_START"])
        subprocess.call(["nssm.exe", "set", "harvester", "AppStdout", "C:\logs\harvester-log.log"])
        subprocess.call(["nssm.exe", "start", "harvester"])
        # check if installation was successful
        time.sleep(1)
        output = str(subprocess.check_output(["nssm.exe", "status", "harvester"]))
        output = output.replace("b'", "")
        output = output.replace("\\r\\n'", "")
        if output == "SERVICE_RUNNING":
            print("Installation reussie")
        else:
            print("L'installeur n'a pas pu installer harvester en tant que service. code d'erreur: " + str(output))
            input("Appuyer sur n'importe quelle touche pour quitter l'installeur")

    @staticmethod
    def windows_is_admin():
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False


if __name__ == "__main__":
    setup = Setup()
