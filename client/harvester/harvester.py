import time
import datetime
import multiprocessing  # multithreading

from devices import *
from databases import *


DEBUG = True


# Main class
class Harvester:
    online = True

    postgres_conn = None
    influx_conn = None

    machine = None
    self_monitor = None
    devices_data = None

    def __init__(self):
        self.connect()
        self.initialize_measurements()
        if self.online:
            self.postgres_send_data()
        self.main_loop()

    # Connect to the databases
    def connect(self):
        try:
            self.postgres_conn = PostgreSQLconn()
            self.influx_conn = InfluxConn()
        except Exception as err:
            print("Can't connect to the database.")
            if DEBUG:
                print(err)
                print("Continue in offline mode ? Y/n")
                if input() == "n":
                    exit()
                self.online = False
                return
            else:
                print("Exiting..")
                input()
                sys.exit()

    # Initialize the measurements
    def initialize_measurements(self):
        self.machine = MachineInfo()
        self.self_monitor = SelfMonitor()
        self.devices_data = {
            "users":        AllUserInfo(),
            "cpu":          CpuInfo(),
            "ram":          RamInfo(),
            "swap":         SWAPInfo(),
            "net_ifaces":   AllNetInterfaceInfo(),
            "partitions":   AllPartitionsInfo(),
            "disks_io":     AllDiskIOInfo(),
            "temp":         AllTempInfo(),
            "fans":         AllFansInfo(),
            "battery":      BatteryInfo(),
        }

    # Send the data to the postgres database
    def postgres_send_data(self):
        self.postgres_conn.get_measurements([
            self.machine,
            self.devices_data["users"],
            self.devices_data["cpu"],
            self.devices_data["ram"],
            self.devices_data["swap"],
            self.devices_data["net_ifaces"],
            self.devices_data["disks_io"]
        ])
        self.postgres_conn.send_data()

    # Main program loop
    def main_loop(self):
        update_n = 0
        while True:
            update_start = datetime.datetime.now()
            if DEBUG:
                print("\nUpdate %s starting at %s\n" % (update_n, update_start.isoformat()))

            self.update_devices()

            update_end = datetime.datetime.now()
            update_duration = (update_end - update_start).total_seconds()
            if DEBUG:
                self.self_monitor.refresh()
                self.self_monitor.print()
                print("\nUpdate %s finished at %s  duration: %s s\n" %
                      (update_n, update_end.isoformat(), round(update_duration, 1)))

            update_n += 1
            time.sleep(5)

    # Update all devices and send the data to InfluxDB
    def update_devices(self):
        for device in self.devices_data:
            if self.devices_data[device].available:
                self.devices_data[device].refresh()
                if self.online:
                    points = self.devices_data[device].make_points()
                    if not self.influx_conn.write_points(points):
                        print("ERROR while updating " + device)
                if DEBUG:
                    self.devices_data[device].print()


if __name__ == "__main__":
    harvester = Harvester()
