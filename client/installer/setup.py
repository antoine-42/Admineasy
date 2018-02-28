import platform
import subprocess
import ctypes
import sys
import os
import time


class Setup:
    def __init__(self):
        # get path
        if getattr(sys, "frozen", False):
            self.dir_path = os.path.dirname(os.path.realpath(sys.executable))
        elif __file__:
            self.dir_path = os.path.dirname(os.path.realpath(__file__))
        self.app_path = self.dir_path.split("harvester-setup")[0]

        # detect OS
        self.os = platform.system()
        if self.os == "Linux":
            self.linux_setup()
        elif self.os == "Windows":
            self.windows_setup()

    def linux_setup(self):
        # put path to executable in service file
        exec_path = os.path.join(self.app_path, "harvester/harvester")
        service_path = os.path.join(self.app_path, 'harvester-setup/admineasy-harvester.service')
        with open(service_path, "r+") as f:
            lines = [line.replace("[EXEC_PATH]", exec_path)
                     if "ExecStart=[EXEC_PATH]" in line else line
                     for line in f]
            f.seek(0)
            f.truncate()
            f.writelines(lines)
        # copy service file, then enable and start it.
        subprocess.call(["/usr/bin/sudo", "mv", service_path, "/etc/systemd/system/"])
        subprocess.call(["/usr/bin/sudo", "systemctl", "enable", "admineasy-harvester.service"])
        subprocess.call(["/usr/bin/sudo", "systemctl", "start", "admineasy-harvester.service"])

    def windows_setup(self):
        # get path to application
        exec_path = os.path.join(self.app_path, "\\harvester\\harvester.exe")
        # get admin privileges
        if not Setup.windows_is_admin():
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, "", None, 1)
        # setup service
        subprocess.call(["nssm.exe", "install", "harvester", exec_path])
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
