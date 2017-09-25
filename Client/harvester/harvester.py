import sys
import collections
import platform  # system info
import psutil  # hardware info
import cpuinfo  # detailed CPU info
# import pySMART  # hard drive smart info, requires admin. DOESNT FUCKING WORK
import influxdb  # communication with influxdb


# DATA COLLECTION
class DiskInfo:
    def __init__(self, device_, mount_, file_system_):  # separer tout
        self.device = device_
        self.mount = mount_
        self.file_system = file_system_

        disk_usage_info = psutil.disk_usage(self.mount)
        self.space_total_B = disk_usage_info[0]
        self.space_available_B = disk_usage_info[2]
        self.space_used_B = disk_usage_info[1]
        self.space_used_percent = disk_usage_info[3]

    def refresh_used(self):
        disk_usage_info = psutil.disk_usage(self.mount)
        self.space_available_B = disk_usage_info[2]
        self.space_used_B = disk_usage_info[1]
        self.space_used_percent = disk_usage_info[3]


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


# Platform
platform_os = platform.platform()
platform_name = platform.node()


# CPU
cpu_info = cpuinfo.get_cpu_info()
cpu_name = cpu_info["brand"]

cpu_logical_cores = psutil.cpu_count()
cpu_physical_cores = psutil.cpu_count(False)
cpu_hyper_threading = True
if cpu_logical_cores == cpu_physical_cores:
    cpu_hyper_threading = False

cpu_freq_info = psutil.cpu_freq()
cpu_freq_curr_mhz = cpu_freq_info[0]
cpu_freq_min_mhz = cpu_freq_info[1]
cpu_freq_max_mhz = cpu_freq_info[2]

cpu_usage_percent = psutil.cpu_percent(1)  # measured between every call, first call meaningless if None

# RAM
ram_info = psutil.virtual_memory()
ram_total_B = ram_info[0]
ram_available_B = ram_info[1]
ram_used_B = ram_info[3]
ram_used_percent = ram_info[2]

# SWAP
swap_info = psutil.swap_memory()
swap_total_B = swap_info[0]
swap_available_B = swap_info[2]
swap_used_B = swap_info[1]
swap_used_percent = swap_info[3]

# Disks
disks_info = psutil.disk_partitions()
disks = []
for curr_disk in disks_info:  # ignore partitions under 1 GB?
    if curr_disk[2] != "":
        disks.append(DiskInfo(curr_disk[0], curr_disk[1], curr_disk[2]))

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


# DB
json_body = [
    {
        "measurement": "cpu_load_short",
        "tags": {
            "machine": platform_name,
            "region": "us-west"
        },
        "time": "2009-11-10T23:00:00Z",
        "fields": {
            "value": 0.64
        }
    }
]
client = influxdb.InfluxDBClient("192.168.1.33", 8086, "admineasy-client", "1337" "admineasy")
# success = client.write_points(json_body)


# DISPLAY
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
