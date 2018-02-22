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

    machine = MachineInfo()

    # Devices Data
    devices_data = {
        "cpu":        CpuInfo(),
        "ram":        RamInfo(),
        "swap":       SWAPInfo(),
        "net_ifaces": AllNetInterfaceInfo(),
        "partitions": AllPartitionsInfo(),
        "disk_io":    AllDiskIOInfo(),
        "temp":       AllTempInfo(),
        "fans":       AllFansInfo(),
        "battery":    BatteryInfo()
    }

    update_n = 0
    while True:
        if DEBUG:
            update_start = datetime.datetime.now()
            print("\nUpdate %s starting at %s\n" % (update_n, update_start.isoformat()))

        for device in devices_data:
            if devices_data[device].available:
                points = devices_data[device].make_points()
                if not influx.write_points(points):
                    print("ERROR while updating " + device)
                if DEBUG:
                    devices_data[device].print()

        if DEBUG:
            update_end = datetime.datetime.now()
            update_duration = (update_end - update_start).total_seconds()
            print("\nUpdate finished at %s  duration: %s s\n" % (update_end.isoformat(), update_duration))

        update_n += 1
        time.sleep(5)
