import time
import datetime
import multiprocessing  # multithreading

from devices import *
from databases import *


DEBUG = True


if __name__ == "__main__":
    # Databases
    postgres = PostgreSQLconn()
    influx = InfluxConn()

    # Devices Data
    machine = MachineInfo()
    devices_data = {
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
        "self_monitor": SelfMonitor()
    }

    postgres.get_measurements([
        machine,
        devices_data["users"],
        devices_data["cpu"],
        devices_data["ram"],
        devices_data["swap"],
        devices_data["net_ifaces"],
        devices_data["disks_io"]
    ])
    postgres.send_data()

    update_n = 0
    while True:
        update_start = datetime.datetime.now()
        if DEBUG:
            print("\nUpdate %s starting at %s\n" % (update_n, update_start.isoformat()))

        for device in devices_data:
            if devices_data[device].available:
                points = devices_data[device].make_points()
                if not influx.write_points(points):
                    print("ERROR while updating " + device)
                if DEBUG:
                    devices_data[device].print()

        update_end = datetime.datetime.now()
        update_duration = (update_end - update_start).total_seconds()
        if DEBUG:
            print("\nUpdate %s finished at %s  duration: %s s\n" %
                  (update_n, update_end.isoformat(), round(update_duration, 3)))

        update_n += 1
        time.sleep(5)
