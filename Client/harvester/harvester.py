import sys
import time
import datetime
import collections
import platform  # system info
import psutil  # hardware info
import cpuinfo  # detailed CPU info
# import pySMART  # hard drive smart info, requires admin. DOESNT FUCKING WORK
import influxdb  # communication with influxdb


# influxDB init
client = influxdb.InfluxDBClient(database="admineasy")

# Platform
platform_os = platform.platform()
platform_name = platform.node()


# DATA COLLECTION
class DiskInfo:
    disk_available_B = -1
    disk_usage_B = -1
    disk_usage_percent = -1

    def __init__(self, device_, mount_, file_system_):  # separer tout
        self.device = device_
        self.mount = mount_
        self.file_system = file_system_

        disk_usage_info = psutil.disk_usage(self.mount)
        self.disk_total_B = disk_usage_info[0]
        self.refresh_used()

    def refresh_used(self):
        disk_usage_info = psutil.disk_usage(self.mount)
        self.disk_available_B = disk_usage_info[2]
        self.disk_usage_B = disk_usage_info[1]
        self.disk_usage_percent = disk_usage_info[3]

    def update_influxdb(self):
        self.refresh()
        json = [
            {
                "measurement": "disk_total_bytes",
                "tags": {
                    "machine": platform_name
                },
                "time": str(datetime.datetime.utcnow().isoformat()),
                "fields": {
                    "value": self.disk_total_B,
                    "partition": self.mount
                }
            },
            {
                "measurement": "disk_available_bytes",
                "tags": {
                    "machine": platform_name
                },
                "time": str(datetime.datetime.utcnow().isoformat()),
                "fields": {
                    "value": self.disk_available_B,
                    "partition": self.mount
                }
            },
            {
                "measurement": "disk_usage_bytes",
                "tags": {
                    "machine": platform_name
                },
                "time": str(datetime.datetime.utcnow().isoformat()),
                "fields": {
                    "value": self.disk_usage_B,
                    "partition": self.mount
                }
            },
            {
                "measurement": "disk_usage_percent",
                "tags": {
                    "machine": platform_name,
                    "partition": self.mount
                },
                "time": str(datetime.datetime.utcnow().isoformat()),
                "fields": {
                    "value": self.disk_usage_percent
                }
            }
        ]
        return client.write_points(json)


class TemperatureSensor:
    def __init__(self, name_, current_, high_, critical_):
        self.name = name_
        self.current = current_
        self.high = high_
        self.critical = critical_

    def is_high(self):
        if self.current >= self.high:
            return True
        return False

    def is_critical(self):
        if self.current >= self.critical:
            return True
        return False


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

    def is_high(self):
        high = 0
        for curr_sensor in self.sensors:
            if curr_sensor.is_high():
                high += 1
        return high

    def is_critical(self):
        critical = 0
        for curr_sensor in self.sensors:
            if curr_sensor.is_critical():
                critical += 1
        return critical

    def highest(self):
        highest = -274
        highest_name = ""
        for curr_sensor in self.sensors:
            if curr_sensor.current > highest:
                highest = curr_sensor.current
                highest_name = curr_sensor.name
        return [highest, highest_name]

    def lowest(self):
        lowest = sys.maxsize
        lowest_name = ""
        for curr_sensor in self.sensors:
            if curr_sensor.current < lowest:
                lowest = curr_sensor.current
                lowest_name = curr_sensor.name
        return [lowest, lowest_name]

    def average(self):
        total = 0
        number = 0
        for curr_sensor in self.sensors:
            total += curr_sensor.current
            number += 1
        return total/number


class RamInfo:
    ram_total_B = -1
    ram_available_B = -1
    ram_used_B = -1
    ram_used_percent = -1

    def __init__(self):
        self.refresh()

    def refresh(self):
        ram_info = psutil.virtual_memory()
        self.ram_total_B = ram_info[0]
        self.ram_available_B = ram_info[1]
        self.ram_used_B = ram_info[3]
        self.ram_used_percent = ram_info[2]

    def update_influxdb(self):
        self.refresh()
        json = [
            {
                "measurement": "ram_total_bytes",
                "tags": {
                    "machine": platform_name
                },
                "time": str(datetime.datetime.utcnow().isoformat()),
                "fields": {
                    "value": self.ram_total_B
                }
            },
            {
                "measurement": "ram_availabe_bytes",
                "tags": {
                    "machine": platform_name
                },
                "time": str(datetime.datetime.utcnow().isoformat()),
                "fields": {
                    "value": self.ram_available_B
                }
            },
            {
                "measurement": "ram_usage_bytes",
                "tags": {
                    "machine": platform_name
                },
                "time": str(datetime.datetime.utcnow().isoformat()),
                "fields": {
                    "value": self.ram_used_B
                }
            },
            {
                "measurement": "ram_usage_percent",
                "tags": {
                    "machine": platform_name
                },
                "time": str(datetime.datetime.utcnow().isoformat()),
                "fields": {
                    "value": self.ram_used_percent
                }
            }
        ]
        return client.write_points(json)


class CpuInfo:
    cpu_freq_curr_mhz = -1

    cpu_usage_percent = -1

    def __init__(self):
        cpu_info = cpuinfo.get_cpu_info()
        self.cpu_name = cpu_info["brand"]

        self.cpu_logical_cores = psutil.cpu_count()
        self.cpu_physical_cores = psutil.cpu_count(False)
        self.cpu_hyper_threading = True
        if self.cpu_logical_cores == self.cpu_physical_cores:
            self.cpu_hyper_threading = False

        cpu_freq_info = psutil.cpu_freq()
        self.cpu_freq_min_mhz = cpu_freq_info[1]
        self.cpu_freq_max_mhz = cpu_freq_info[2]

        self.refresh()

    def refresh(self):
        cpu_freq_info = psutil.cpu_freq()
        self.cpu_freq_curr_mhz = cpu_freq_info[0]

        # measured between every call, first call meaningless if None then average between every call
        self.cpu_usage_percent = psutil.cpu_percent(1)

    def update_influxdb(self):
        self.refresh()
        json = [
            {
                "measurement": "cpu_freq_mhz",
                "tags": {
                    "machine": platform_name
                },
                "time": str(datetime.datetime.utcnow().isoformat()),
                "fields": {
                    "value": self.cpu_freq_curr_mhz
                }
            },
            {
                "measurement": "cpu_usage_percent",
                "tags": {
                    "machine": platform_name
                },
                "time": str(datetime.datetime.utcnow().isoformat()),
                "fields": {
                    "value": self.cpu_usage_percent
                }
            }
        ]
        return client.write_points(json)


# SWAP
swap_info = psutil.swap_memory()
swap_total_B = swap_info[0]
swap_available_B = swap_info[2]
swap_used_B = swap_info[1]
swap_used_percent = swap_info[3]


# Sensors
temp_devices = []
temp_unavailable = False
if hasattr(psutil, "sensors_temperatures"):
    temp_info = psutil.sensors_temperatures()
    if temp_info is not None:
        for device_name, sensors in temp_info.items():
            temp_devices.append(TemperatureDevice(device_name, sensors))
    else:
        temp_unavailable = True

fans_info = None
if hasattr(psutil, "sensors_fans"):
    fans_info = psutil.sensors_fans()
battery_info = psutil.sensors_battery()

# Other stuff
boot_timestamp = psutil.boot_time()


# todo: create user "admineasy-client", "1337", . 192.168.1.33


# DISPLAY
'''
print('\n' + "System")
print("OS: " + platform_os)
print("Machine name: " + platform_name)

print('\n' + "CPU")
cpu_text = cpu_name + "  @" + str(round(cpu_freq_max_mhz/1000, 1)) + "Ghz"
cpu_text += "  (current: " + str(round(cpu_freq_max_mhz/1000, 1)) + "Ghz)    " + str(cpu_logical_cores)
if cpu_hyper_threading:
    cpu_text += " Logical cores  " + str(cpu_physical_cores) + " Physical"
cpu_text += " cores    Usage: " + str(cpu_usage_percent) + "%"
print(cpu_text)

print('\n' + "RAM")
print("Total: " + str(round(ram_total_B/1000000000, 1)) + "GB  Used: " + str(ram_used_percent) + "%")

print('\n' + "SWAP")
print("Total: " + str(round(swap_total_B/1000000000, 1)) + "GB  Used: " + str(swap_used_percent) + "%")

print('\n' + "Disks")
for disk in disks:
    disk_text = disk.device
    if disk.mount != disk.device:
        disk_text += "  (" + disk.mount + ")"
    disk_text += "    File System: " + disk.file_system
    disk_text += "    Total space: " + str(round(disk.space_total_B/1000000000, 1)) + "GB"
    disk_text += "  Used: " + str(disk.space_used_percent) + "%"
    print(disk_text)

print('\n' + "Temperature")
if len(temp_devices) == 0:
    if temp_unavailable:
        print("Temperature information unavailable on this system")
    else:
        print("No temperature sensor was detected")
else:
    for device in temp_devices:
        device_text = ""

        if device.type != "":
            device_text += device.type
        else:
            device_text += device.name

        device_text += "    Average: " + str(round(device.average(), 1)) + "C"

        if device.is_critical():
            device_text += "  TEMPERATURE CRITICAL"
        elif device.is_high():
            device_text += "  Temperature high"

        print(device_text)

print('\n' + "Fans")
if fans_info is None:
    print("Fan speed information unavailable")
else:
    if len(fans_info) == 0:
        print("No fan detected")
    else:
        for fan in fans_info:
            print(fan[0] + ": " + fan[1] + "RPM")
'''


ram = RamInfo()
cpu = CpuInfo()

# Disks
disks_info = psutil.disk_partitions()
disks = []
for curr_disk in disks_info:  # ignore partitions under 1 GB?
    if curr_disk[2] != "":
        disks.append(DiskInfo(curr_disk[0], curr_disk[1], curr_disk[2]))


while True:
    ram.update_influxdb()
    cpu.update_influxdb()

    for disk in disks:
        disk.update_influxdb()

    time.sleep(5)
