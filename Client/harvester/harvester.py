import sys
import time
import datetime
import collections
import platform  # system info
import psutil  # hardware info
import cpuinfo  # detailed CPU info
# import pySMART  # hard drive smart info, requires admin. DOESNT FUCKING WORK
import influxdb  # communication with influxdb


#########################################
#                CLASSES                #
#########################################
class UserInfo:
    start = time.time() # Timestamp of the first connection of this user

    def __init__(self, name_):
        self.name = name_
        self.sessions = 1
        self.refresh()

    # Updates all the data.
    def refresh(self):
        users_info = psutil.users()
        self.sessions = 0
        for user_info in users_info:
            if user_info[0] == self.name:
                self.sessions += 1
                if user_info[3] < self.start:
                    self.start = user_info[3]


class CpuInfo:
    # todo: per core frequency and usage
    freq_curr_mhz = -1
    used_percent = -1

    def __init__(self):
        cpu_info = cpuinfo.get_cpu_info()
        self.name = cpu_info["brand"]

        self.logical_cores = psutil.cpu_count()
        self.physical_cores = psutil.cpu_count(False)
        self.hyper_threading = True
        if self.logical_cores == self.physical_cores:
            self.hyper_threading = False

        freq_info = psutil.cpu_freq()
        self.freq_min_mhz = freq_info[1]
        self.freq_max_mhz = freq_info[2]

        self.refresh()

    # Updates all the data.
    def refresh(self):
        freq_info = psutil.cpu_freq()
        self.freq_curr_mhz = freq_info[0]

        # measured between every call, first call meaningless if None then average between every call
        self.used_percent = psutil.cpu_percent(1)

    # Updates all the data, then sends it to the influxdb database.
    def update_influxdb(self):
        self.refresh()
        json = [
            {
                "measurement": "cpu",
                "tags": {
                    "machine": platform_name
                },
                "time": str(datetime.datetime.utcnow().isoformat()),
                "fields": {
                    "freq": self.freq_curr_mhz,
                    "used": self.used_percent
                }
            }
        ]
        return client.write_points(json)


class RamInfo:
    total_B = -1
    available_B = -1
    used_B = -1
    used_percent = -1

    def __init__(self):
        self.refresh()

    # Updates all the data.
    def refresh(self):
        ram_info = psutil.virtual_memory()
        self.total_B = ram_info[0]
        self.available_B = ram_info[1]
        self.used_B = ram_info[3]
        self.used_percent = ram_info[2]

    # Updates all the data, then sends it to the influxdb database.
    def update_influxdb(self):
        self.refresh()
        json = [
            {
                "measurement": "ram",
                "tags": {
                    "machine": platform_name
                },
                "time": str(datetime.datetime.utcnow().isoformat()),
                "fields": {
                    "total_bytes": self.total_B,
                    "available_bytes": self.available_B,
                    "used_bytes": self.used_B,
                    "used_percent": self.used_percent
                }
            }
        ]
        return client.write_points(json)


class SWAPInfo:
    swap_total_B = -1
    swap_available_B = -1
    swap_used_B = -1
    swap_used_percent = -1

    def __init__(self):
        self.refresh()

    # Updates all the data.
    def refresh(self):
        swap_info = psutil.swap_memory()
        self.swap_total_B = swap_info[0]
        self.swap_available_B = swap_info[2]
        self.swap_used_B = swap_info[1]
        self.swap_used_percent = swap_info[3]

    # Updates all the data, then sends it to the influxdb database.
    def update_influxdb(self):
        self.refresh()
        json = [
            {
                "measurement": "swap",
                "tags": {
                    "machine": platform_name
                },
                "time": str(datetime.datetime.utcnow().isoformat()),
                "fields": {
                    "total_bytes": self.swap_total_B,
                    "available_bytes": self.swap_available_B,
                    "used_bytes": self.swap_used_B,
                    "used_percent": self.swap_used_percent
                }
            }
        ]
        return client.write_points(json)


class InterfaceInfo:
    sent_B = -1
    sent_packets = -1
    out_error = -1
    out_drop = -1
    received_B = -1
    received_packets = -1
    in_error = -1
    in_drop = -1

    def __init__(self, name_):
        self.name = name_

        interfaces_info = psutil.net_if_stats()
        for interface_name, interface_info in interfaces_info.items():
            if interface_name == self.name:
                self.up = interface_info[0]
                self.speed = interface_info[2]
                self.mtu = interface_info[3]
                break

        self.refresh()

    # Updates all the data.
    def refresh(self):
        counters_info = psutil.net_io_counters()

        self.sent_B = counters_info[0]
        self.sent_packets = counters_info[2]

        self.received_B = counters_info[1]
        self.received_packets = counters_info[3]

        self.out_error = counters_info[5]
        self.out_drop = counters_info[7]

        self.in_error = counters_info[4]
        self.in_drop = counters_info[6]

    # Updates all the data, then sends it to the influxdb database.
    def update_influxdb(self):
        self.refresh()
        json = [
            {
                "measurement": "network",
                "tags": {
                    "machine": platform_name,
                    "interface": self.name
                },
                "time": str(datetime.datetime.utcnow().isoformat()),
                "fields": {
                    "sent_bytes": self.sent_B,
                    "sent_packets": self.sent_packets,
                    "received_bytes": self.received_B,
                    "received_packets": self.received_packets,
                    "out_error": self.out_error,
                    "out_drop": self.out_drop,
                    "in_error": self.in_error,
                    "in_drop": self.in_drop
                }
            }
        ]
        return client.write_points(json)


class DiskInfo:
    total_B = -1
    available_B = -1
    used_B = -1
    used_percent = -1

    read_bytes = -1
    read_count = -1
    read_time = -1
    write_bytes = -1
    write_count = -1
    write_time = -1

    def __init__(self, device_, mount_, file_system_):  # separer tout
        self.device = device_
        self.mount = mount_
        self.file_system = file_system_

        self.refresh_used()

    # Updates all the data.
    def refresh(self):
        self.refresh_used()
        self.refresh_io()
        # refresh smart

    # Updates the used space data.
    def refresh_used(self):
        disk_used_info = psutil.disk_usage(self.mount)
        self.total_B = disk_used_info[0]
        self.available_B = disk_used_info[2]
        self.used_B = disk_used_info[1]
        self.used_percent = disk_used_info[3]

    def refresh_io(self):
        disks_io_info = psutil.disk_io_counters(True)
        for disk_name, disk_io_info in disks_io_info.items():
            if disk_name == self.device:  # TODO doesn't works on windows, use global?
                self.read_bytes = disk_io_info[2]
                self.read_count = disk_io_info[0]
                self.read_time = disk_io_info[4]
                self.write_bytes = disk_io_info[3]
                self.write_count = disk_io_info[1]
                self.write_time = disk_io_info[5]
                break

    # Updates all the data, then sends it to the influxdb database.
    def update_influxdb(self):
        self.refresh()
        json = [
            {
                "measurement": "disk",
                "tags": {
                    "machine": platform_name,
                    "partition": self.device.replace("\\", "")
                },
                "time": str(datetime.datetime.utcnow().isoformat()),
                "fields": {
                    "total": self.total_B,
                    "available": self.available_B,
                    "used": self.used_B,
                    "used_percent": self.used_percent
                }
            },
            {
                "measurement": "disk_io",
                "tags": {
                    "machine": platform_name,
                    "partition": self.device.replace("\\", "")
                },
                "time": str(datetime.datetime.utcnow().isoformat()),
                "fields": {
                    "read_bytes": self.read_bytes,
                    "read_count": self.read_count,
                    "read_time": self.read_time,
                    "write_bytes": self.write_bytes,
                    "write_count": self.write_count,
                    "write_time": self.write_time
                }
            }
        ]
        return client.write_points(json)


class TemperatureDevice:
    name_to_device = collections.defaultdict(str)
    name_to_device_list = [
        ["coretemp", "CPU"],
        ["acpitz", "motherboard"]
    ]

    def __init__(self, name_, sensors_):
        for k, v in self.name_to_device_list:
            self.name_to_device[k] = v

        self.name = name_
        self.type = self.name_to_device[self.name]
        self.sensors = []
        for curr_sensor in sensors_:
            self.sensors.append(TemperatureSensor(curr_sensor[0], curr_sensor[1], curr_sensor[2], curr_sensor[3]))

    # Returns the number of sensors in high temperature range (not including critical).
    def is_high(self):
        high = 0
        for curr_sensor in self.sensors:
            if curr_sensor.is_high() and not curr_sensor.is_critical():
                high += 1
        return high

    # Returns the number of sensors in critical temperature range.
    def is_critical(self):
        critical = 0
        for curr_sensor in self.sensors:
            if curr_sensor.is_critical():
                critical += 1
        return critical

    # Returns a table with the highest temperature and the name of the sensor that recorded it.
    def highest(self):
        highest = -274
        highest_name = ""
        for curr_sensor in self.sensors:
            if curr_sensor.current > highest:
                highest = curr_sensor.current
                highest_name = curr_sensor.name
        return [highest, highest_name]

    # Returns a table with the lowest temperature and the name of the sensor that recorded it.
    def lowest(self):
        lowest = sys.maxsize
        lowest_name = ""
        for curr_sensor in self.sensors:
            if curr_sensor.current < lowest:
                lowest = curr_sensor.current
                lowest_name = curr_sensor.name
        return [lowest, lowest_name]

    # Returns the average of all the temperatures recorded by every sensors.
    def average(self):
        total = 0
        number = 0
        for curr_sensor in self.sensors:
            total += curr_sensor.current
            number += 1
        return total/number

    # Updates all the data.
    def refresh(self):
        pass
        # todo

    # Updates all the data, then sends it to the influxdb database.
    def update_influxdb(self):
        self.refresh()

        json = [
            {
                "measurement": "temp",
                "tags": {
                    "machine": platform_name,
                    "device": self.name
                },
                "time": str(datetime.datetime.utcnow().isoformat()),
                "fields": {
                    "average": self.average(),
                    "highest": self.highest()[0],
                    "lowest": self.lowest()[1],
                    "is_high": self.is_high(),
                    "is_critical": self.is_critical()
                }
            }
        ]

        for sensor in sensors:
            json.append({
                "measurement": "temp_advanced",
                "tags": {
                    "machine": platform_name,
                    "device": self.name,
                    "sensor": sensor.name
                },
                "time": str(datetime.datetime.utcnow().isoformat()),
                "fields": {
                    "current": sensor.current,
                    "high": sensor.high,
                    "critical": sensor.critical
                }
            })

        return client.write_points(json)


class TemperatureSensor:
    def __init__(self, name_, current_, high_, critical_):
        self.name = name_
        self.current = current_
        self.high = high_
        self.critical = critical_

    # Returns True if the sensor is in high temperature range, false otherwise.
    def is_high(self):
        if self.current >= self.high:
            return True
        return False

    # Returns True if the sensor is in critical temperature range, false otherwise.
    def is_critical(self):
        if self.current >= self.critical:
            return True
        return False


class FanInfo:
    rpm = -1

    def __init__(self, name_):
        self.name = name_
        self.refresh()

    # Updates all the data.
    def refresh(self):
        for curr_fan in psutil.sensors_fans():
            if curr_fan[0] == self.name:
                self.rpm = curr_fan[0]
                break

    # Updates all the data, then sends it to the influxdb database.
    def update_influxdb(self):
        self.refresh()
        json = [
            {
                "measurement": "fan",
                "tags": {
                    "machine": platform_name,
                    "device": self.name
                },
                "time": str(datetime.datetime.utcnow().isoformat()),
                "fields": {
                    "rpm": self.rpm
                }
            }
        ]
        return client.write_points(json)


class BatteryInfo:
    available = True

    is_plugged = True
    percent_left = -1
    seconds_left = -1

    def __init__(self):
        if psutil.sensors_battery() is None:
            self.available = False
        else:
            self.refresh()

    # Updates all the data.
    def refresh(self):
        battery_info = psutil.sensors_battery()
        self.is_plugged = battery_info[2]
        self.percent_left = battery_info[0]
        self.seconds_left = battery_info[1]

    # Updates all the data, then sends it to the influxdb database.
    def update_influxdb(self):
        self.refresh()
        json = [
            {
                "measurement": "fan",
                "tags": {
                    "machine": platform_name
                },
                "time": str(datetime.datetime.utcnow().isoformat()),
                "fields": {
                    "is_plugged": self.is_plugged,
                    "percent_left": self.percent_left,
                    "seconds_left": self.seconds_left
                }
            }
        ]
        return client.write_points(json)


######################################
#                Init                #
######################################
# InfluxDB
# todo: create user "admineasy-client", "1337"
# client = influxdb.InfluxDBClient(database="admineasy")
client = influxdb.InfluxDBClient(host="192.168.1.33", database="admineasy", username="admineasy-client", password="1337")

# Platform
platform_os = platform.platform()
platform_name = platform.node()

users_info = psutil.users()
users = []
for user_info in users_info:
    users.append(UserInfo(user_info[0]))

boot_timestamp = psutil.boot_time()

# Devices Data
cpu = CpuInfo()
ram = RamInfo()
swap = SWAPInfo()

interfaces = []
interfaces_info = psutil.net_if_stats()
for interface_name, interface_info in interfaces_info.items():
    interfaces.append(InterfaceInfo(interface_name))

disks_info = psutil.disk_partitions()
disks = []
for curr_disk in disks_info:  # ignore partitions under 1 GB?
    if curr_disk[2] != "":
        disks.append(DiskInfo(curr_disk[0], curr_disk[1], curr_disk[2]))

temp_devices = []
temp_unavailable = False
if hasattr(psutil, "sensors_temperatures"):
    temp_info = psutil.sensors_temperatures()
    if temp_info is not None:
        for device_name, sensors in temp_info.items():
            temp_devices.append(TemperatureDevice(device_name, sensors))
    else:
        temp_unavailable = True

fans = []
if hasattr(psutil, "sensors_fans"):
    fans_info = psutil.sensors_fans()
    for curr_fan_info in fans_info:
        fans.append(FanInfo(curr_fan_info[0]))

battery = BatteryInfo()


###########################################
#                Execution                #
###########################################
while True:
    cpu.update_influxdb()
    ram.update_influxdb()
    swap.update_influxdb()

    for interface in interfaces:
        interface.update_influxdb()

    for disk in disks:
        disk.update_influxdb()

    for temp_device in temp_devices:
        temp_device.update_influxdb()

    for fan in fans:
        fan.update_influxdb()

    if battery.available:
        battery.update_influxdb()

    time.sleep(5)
