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
    # TODO: per core frequency and usage
    freq_curr_mhz = -1
    used_percent = -1

    def __init__(self):
        # Name
        cpu_info = cpuinfo.get_cpu_info()
        self.name = cpu_info["brand"]

        # Core info
        self.logical_cores = psutil.cpu_count()
        self.physical_cores = psutil.cpu_count(False)
        self.hyper_threading = True
        if self.logical_cores == self.physical_cores:
            self.hyper_threading = False

        # Frequency
        freq_info = psutil.cpu_freq()
        self.freq_min_mhz = freq_info[1]
        self.freq_max_mhz = freq_info[2]

        self.refresh()

    # Updates all the data.
    def refresh(self):
        freq_info = psutil.cpu_freq()
        self.freq_curr_mhz = freq_info[0]

        # measured between every call, if None first call meaningless then average between every call
        self.used_percent = psutil.cpu_percent(1)

    # Updates all the data, then sends it to the influxdb database.
    def update_influxdb(self):
        self.refresh()
        json = [
            {
                "measurement": "cpu",
                "tags": {
                    "machine": machine_name
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
                    "machine": machine_name
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
    total_B = -1
    available_B = -1
    used_B = -1
    used_percent = -1

    input_B = -1
    output_B = -1

    def __init__(self):
        self.refresh()

    # Updates all the data.
    def refresh(self):
        swap_info = psutil.swap_memory()
        self.total_B = swap_info[0]
        self.available_B = swap_info[2]
        self.used_B = swap_info[1]
        self.used_percent = swap_info[3]

        self.input_B = swap_info[4]
        self.output_B = swap_info[5]

    # Updates all the data, then sends it to the influxdb database.
    def update_influxdb(self):
        self.refresh()
        json = [
            {
                "measurement": "swap",
                "tags": {
                    "machine": machine_name
                },
                "time": str(datetime.datetime.utcnow().isoformat()),
                "fields": {
                    "total_bytes": self.total_B,
                    "available_bytes": self.available_B,
                    "used_bytes": self.used_B,
                    "used_percent": self.used_percent,
                    "input_bytes": self.input_B,
                    "output_bytes": self.output_B
                }
            }
        ]
        return client.write_points(json)


class NetInterfaceInfo:
    # TODO: data collection for all interfaces
    sent_B = -1
    sent_packets = -1
    received_B = -1
    received_packets = -1
    total_B = -1  # Grafana doesn't support operations on multiple sources, so this has to be done here.....
    total_packets = -1

    out_error = -1
    out_drop = -1
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

        self.total_B = self.sent_B + self.received_B
        self.total_packets = self.sent_packets + self.received_packets

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
                    "machine": machine_name,
                    "interface": self.name
                },
                "time": str(datetime.datetime.utcnow().isoformat()),
                "fields": {
                    "sent_bytes": self.sent_B,
                    "sent_packets": self.sent_packets,
                    "received_bytes": self.received_B,
                    "received_packets": self.received_packets,
                    "total_bytes": self.total_B,
                    "total_packets": self.total_packets,

                    "out_error": self.out_error,
                    "out_drop": self.out_drop,
                    "in_error": self.in_error,
                    "in_drop": self.in_drop
                }
            }
        ]
        return client.write_points(json)


class PartitionInfo:
    total_B = -1
    available_B = -1
    used_B = -1
    used_percent = -1

    def __init__(self, device_):
        self.device = device_

        for partition in psutil.disk_partitions():
            if partition[0] == self.device:
                self.mount = partition[1]
                self.file_system = partition[2]
                self.options = partition[3]

        self.refresh()

    # Updates all the data.
    def refresh(self):
        self.refresh_used()
        # self.refresh_smart()

    # Updates the used space data.
    def refresh_used(self):
        partition_used_info = psutil.disk_usage(self.mount)
        self.total_B = partition_used_info[0]
        self.available_B = partition_used_info[2]
        self.used_B = partition_used_info[1]
        self.used_percent = partition_used_info[3]

    # Updates the SMART data.
    def refresh_smart(self):
        # TODO
        pass

    # Updates all the data, then sends it to the influxdb database.
    def update_influxdb(self):
        self.refresh()
        json = [
            {
                "measurement": "partition",
                "tags": {
                    "machine": machine_name,
                    "partition": self.device.replace("\\", "")
                },
                "time": str(datetime.datetime.utcnow().isoformat()),
                "fields": {
                    "total": self.total_B,
                    "available": self.available_B,
                    "used": self.used_B,
                    "used_percent": self.used_percent
                }
            }
        ]
        return client.write_points(json)


class DiskIOInfo:
    read_bytes = -1
    read_count = -1
    read_time = -1
    write_bytes = -1
    write_count = -1
    write_time = -1

    def __init__(self, physical_drive_):
        self.physical_drive = physical_drive_
        self.refresh()

    # Updates all the data.
    def refresh(self):
        disks_io_info = psutil.disk_io_counters(True)
        for disk_name, disk_io_info in disks_io_info.items():
            if disk_name == self.physical_drive:
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
                "measurement": "disk_io",
                "tags": {
                    "machine": machine_name,
                    "disk": self.physical_drive
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

    def __init__(self, name_):
        # Init name_to_device_list
        for k, v in self.name_to_device_list:
            self.name_to_device[k] = v

        self.name = name_
        # Get a type from the generic name
        self.type = self.name_to_device[self.name]

        # if a type is set, use that for the clean name
        self.clean_name = self.name
        if self.type != "":
            self.clean_name = self.type

        # Init the sensors
        devices_info = psutil.sensors_temperatures()
        for device_name, sensors_info in devices_info.items():
            if device_name == self.name:
                self.sensors = [TemperatureSensor(
                    sensor_info[0], sensor_info[1], sensor_info[2], sensor_info[3]
                ) for sensor_info in sensors_info]
                break

    # Returns the number of sensors in high temperature range (not including critical).
    def high(self):
        high = 0
        for curr_sensor in self.sensors:
            if curr_sensor.is_high() and not curr_sensor.is_critical():
                high += 1
        return high

    # Returns the number of sensors in critical temperature range.
    def critical(self):
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
        updated_devices_info = psutil.sensors_temperatures()
        for updated_device_name, updated_sensors in updated_devices_info.items():
            if updated_device_name == self.name:

                for updated_sensor in updated_sensors:
                    for sensor in self.sensors:
                        if sensor.name == updated_sensor[0]:
                            sensor.refresh(updated_sensor)
                break

    # Updates all the data, then sends it to the influxdb database.
    def update_influxdb(self):
        self.refresh()
        # Basic temp info, for every device
        json = [
            {
                "measurement": "temp",
                "tags": {
                    "machine": machine_name,
                    "device": self.clean_name
                },
                "time": str(datetime.datetime.utcnow().isoformat()),
                "fields": {
                    "average": self.average(),
                    "highest": self.highest()[0],
                    "lowest": self.lowest()[0],
                    "high": self.high(),
                    "critical": self.critical()
                }
            }
        ]
        # Advanced temp info, for every sensor
        for sensor in self.sensors:
            json.append({
                "measurement": "temp_advanced",
                "tags": {
                    "machine": machine_name,
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
    def __init__(self, name_, current_=-1, high_=-1, critical_=-1):
        self.name = name_
        self.current = current_
        self.high = high_
        self.critical = critical_

    # Updates all the data.
    def refresh(self, data):
        self.current = data[1]
        self.high = data[2]
        self.critical = data[3]

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
                    "machine": machine_name,
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
                "measurement": "battery",
                "tags": {
                    "machine": machine_name
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
client = influxdb.InfluxDBClient(database="admineasy") # todo: create user "admineasy-client", "1337"
# client = influxdb.InfluxDBClient(host="192.168.1.33", database="admineasy", username="admineasy-client", password="1337")

# Platform
platform_os_name = platform.system()
platform_os_version = platform.release()
platform_os_full = platform.platform()
machine_name = platform.node()

users_info = psutil.users()
users = []
for user_info in users_info:
    users.append(UserInfo(user_info[0]))

boot_timestamp = psutil.boot_time()

# Devices Data
cpu = CpuInfo()
ram = RamInfo()
swap = SWAPInfo()

interfaces_info = psutil.net_if_stats()
interfaces = [NetInterfaceInfo(interface_name) for interface_name, interface_info in interfaces_info.items()]

partitions_info = psutil.disk_partitions()
partitions = []
for curr_partition in partitions_info:  # ignore partitions under 1 GB?
    if curr_partition[2] != "":
        partitions.append(PartitionInfo(curr_partition[0]))

disks_io_info = psutil.disk_io_counters(True)
disks_io = [DiskIOInfo(disk_name) for disk_name, disks_io_info in disks_io_info.items()]

temp_devices = []
temp_unavailable = False
if hasattr(psutil, "sensors_temperatures"):
    sensors_info = psutil.sensors_temperatures()
    if sensors_info is not None:
        temp_devices = [TemperatureDevice(device_name) for device_name, sensors in sensors_info.items()]
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

    for partition in partitions:
        partition.update_influxdb()

    for disk_io in disks_io:
        disk_io.update_influxdb()

    for temp_device in temp_devices:
        temp_device.update_influxdb()

    for fan in fans:
        fan.update_influxdb()

    if battery.available:
        battery.update_influxdb()

    time.sleep(5)
