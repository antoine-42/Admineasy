import time
import datetime
import multiprocessing  # multithreading
import json

from devices import *
from databases import *


# Main class
class Harvester:
    debug = True
    online = True

    postgres_options = None
    influx_options = None
    postgres_conn = None
    influx_conn = None

    machine = None
    self_monitor = None
    devices_data = None

    def __init__(self):
        self.import_settings()
        self.check_args()
        self.connect()
        self.initialize_measurements()
        if self.online:
            self.postgres_send_data()
        self.main_loop()

    # check command line args
    def check_args(self):
        if sys.argv[0] == "-d":
            self.debug = True

    def import_settings(self):
        with open('settings.json', 'r') as f:
            settings = json.load(f)
        try:
            self.debug = settings["options"]["debug"]
            self.postgres_options = settings["postgres"]
            self.influx_options = settings["influx"]
        except KeyError as e:
            print("Error while opening the configuration file:")
            print(e)

    # Connect to the databases
    def connect(self):
        try:
            if self.debug:
                print("Connecting to PostgreSQL: %s@%s" %
                      (self.postgres_options["login"], self.postgres_options["host"]))
            self.postgres_conn = PostgreSQLconn(self.postgres_options)
            if self.debug:
                print("Connecting to InfluxDB: %s@%s" %
                      (self.influx_options["login"], self.influx_options["host"]))
            self.influx_conn = InfluxConn(self.influx_options)
        except Exception as err:
            print("Can't connect to the database:")
            if self.debug:
                print(err)
                print("Continue in offline mode ? Y/n")
                if input() == "n":
                    exit()
                self.online = False
                return
            else:
                print("Exiting...")
                sys.exit()

    # Initialize the measurements
    def initialize_measurements(self):
        if self.debug:
            print("Initializing measurements")
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
        if self.debug:
            print("Sending data to postgreSQL database")
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
        if self.debug:
            print("Initialisation finished.")
        update_n = 0
        while True:
            update_start = datetime.datetime.now()
            if self.debug:
                print("\nUpdate %s starting at %s\n" % (update_n, update_start.isoformat()))

            self.update_devices()

            update_end = datetime.datetime.now()
            update_duration = (update_end - update_start).total_seconds()
            if self.debug:
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
                if self.debug:
                    self.devices_data[device].print()


if __name__ == "__main__":
    harvester = Harvester()
