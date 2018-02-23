import sys
import time
import datetime
import collections  # for default dict
import platform  # System info.
import os  # System info.
import socket  # Used to get IP.

# External libraries
import psutil  # Hardware info.
import cpuinfo  # Detailed CPU info.
# import pySMART  # Hard drive SMART info, requires admin. DOESNT FUCKING WORK. TODO make it work

MACHINE_NAME = platform.node()


# Get basic information on the machine.
class MachineInfo:
    def __init__(self):
        self.name = platform.node()

        self.os_name = platform.system()
        self.os_version = platform.release()
        self.os_full = platform.platform()

        self.boot_timestamp = psutil.boot_time()

    def print(self):
        print("Machine name: %s  OS: %s" % (self.name, self.os_full))


# Monitors harvester.
class SelfMonitor:
    cpu_percent = -1
    ram_percent = -1

    def __init__(self):
        self.pid = os.getpid()
        self.process = psutil.Process(self.pid)
        self.process.cpu_percent()  # throw away data from the first call, it's meaningless.

        self.refresh()

    # Updates all the data.
    def refresh(self):
        with self.process.oneshot():
            self.cpu_percent = self.process.cpu_percent()
            self.ram_percent = self.process.memory_percent()

    # Make points to send to influxdb.
    def make_points(self):
        return [
            {
                "measurement": "self_monitor",
                "tags": {
                    "machine": MACHINE_NAME
                },
                "time": str(datetime.datetime.now().isoformat()),
                "fields": {
                    "cpu_percent": self.cpu_percent,
                    "ram_percent": self.ram_percent
                }
            }
        ]

    def print(self):
        print("Self usage:  CPU: %s %%  RAM: %s %%" %
              (round(self.cpu_percent, 2), round(self.ram_percent, 2)))


# Parent class for all monitors
class DeviceInfo:
    available = True


# Monitors all connected users
class AllUserInfo(DeviceInfo):
    def __init__(self):
        self.users = [UserInfo(user_name)
                      for user_name, user_info1, user_info2, user_info3, user_info4
                      in psutil.users()]

    # Updates all the data.
    def refresh(self):
        users_init = psutil.users()
        for user_init in users_init:
            found = False
            for user_info in self.users:
                if user_init[0] == user_info.name:
                    found = True
                    break
            if not found:
                self.users.append(UserInfo(user_init[0]))

    # Make points to send to influxdb.
    def make_points(self):
        user_dict = {}
        for user in self.users:
            user_dict[user.name] = user.start
        return [
            {
                "measurement": "users",
                "tags": {
                    "machine": MACHINE_NAME
                },
                "time": str(datetime.datetime.now().isoformat()),
                "fields": user_dict
            }
        ]

    # Prints the information on all users
    def print(self):
        for user in self.users:
            user.print()


# Monitors 1 session
class UserInfo:
    def __init__(self, name_):
        self.name = name_
        min_time = time.time()
        users = psutil.users()
        for user in users:
            if self.name == user.name and min_time > user.started:
                min_time = user.started
        self.start = datetime.datetime.utcfromtimestamp(min_time).isoformat()

    # Prints the information on 1 user
    def print(self):
        print("User: %s  connected at: %s" % (self.name, self.start))


# Get information on the CPU
class CpuInfo(DeviceInfo):
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

    # Make points to send to influxdb.
    def make_points(self):
        return [
            {
                "measurement": "cpu",
                "tags": {
                    "machine": MACHINE_NAME
                },
                "time": str(datetime.datetime.now().isoformat()),
                "fields": {
                    "freq": self.freq_curr_mhz,
                    "used": self.used_percent
                }
            }
        ]

    # Prints the information on the CPU
    def print(self):
        print("CPU: %s  Cores: %d  Hyperthreading: %s  Usage: %s %%  Frequency: %s mhz" %
              (self.name, self.physical_cores, self.hyper_threading, self.used_percent, round(self.freq_curr_mhz, 0)))


# Get information on RAM usage.
class RamInfo(DeviceInfo):
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

    # Make points to send to influxdb.
    def make_points(self):
        return [
            {
                "measurement": "ram",
                "tags": {
                    "machine": MACHINE_NAME
                },
                "time": str(datetime.datetime.now().isoformat()),
                "fields": {
                    "total_bytes": self.total_B,
                    "available_bytes": self.available_B,
                    "used_bytes": self.used_B,
                    "used_percent": self.used_percent
                }
            }
        ]

    # Prints the information on RAM usage
    def print(self):
        print("RAM: %s GB  Used: %s GB (%s %%)" %
              (round(self.total_B / 1000000000, 1), round(self.used_B / 1000000000, 1), self.used_percent))


# Get information on SWAP usage.
class SWAPInfo(DeviceInfo):
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

    # Make points to send to influxdb.
    def make_points(self):
        return [
            {
                "measurement": "swap",
                "tags": {
                    "machine": MACHINE_NAME
                },
                "time": str(datetime.datetime.now().isoformat()),
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

    # Prints the information on SWAP usage
    def print(self):
        print("SWAP: %s GB  Used: %s GB (%s %%)" %
              (round(self.total_B / 1000000000, 1), round(self.used_B / 1000000000, 1), self.used_percent))


# Monitors all network interfaces.
class AllNetInterfaceInfo(DeviceInfo):
    def __init__(self):
        interfaces_init_info = psutil.net_if_stats()
        self.interfaces = [NetInterfaceInfo(interface_name)
                           for interface_name, interface_info
                           in interfaces_init_info.items()]
        self.localIP = socket.gethostbyname(socket.gethostname())

    # Get the names of all interfaces
    def get_names(self):
        names = ""
        for interface in self.interfaces:
            names += interface.name
        return names

    # Updates all the data.
    def refresh(self):
        for interface in self.interfaces:
            interface.refresh()

    # Make points to send to influxdb.
    def make_points(self):
        json = []
        for interface in self.interfaces:
            json.append(interface.make_points())
        return json

    # Prints the information on all network interfaces
    def print(self):
        for interface in self.interfaces:
            interface.print()


# Monitors 1 network interfaces.
class NetInterfaceInfo:
    sent_B = -1
    sent_packets = -1
    received_B = -1
    received_packets = -1

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

        self.sent_B = int(counters_info[0] / 8)
        self.sent_packets = counters_info[2]

        self.received_B = int(counters_info[1] / 8)
        self.received_packets = counters_info[3]

        self.out_error = counters_info[5]
        self.out_drop = counters_info[7]

        self.in_error = counters_info[4]
        self.in_drop = counters_info[6]

    #  Make points to send to parent class.
    def make_points(self):
        return {
            "measurement": "network",
            "tags": {
                "machine": MACHINE_NAME,
                "interface": self.name
            },
            "time": str(datetime.datetime.now().isoformat()),
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

    # Prints the information on 1 network interface
    def print(self):
        print("Interface: %s    received: %s MB  sent: %s MB  errors: %d" %
              (self.name, round(self.received_B / 1000000, 1), round(self.sent_B / 1000000, 1),
               self.in_error+self.out_drop+self.out_drop+self.in_drop))


# Monitors the usage of all partitions.
class AllPartitionsInfo(DeviceInfo):
    def __init__(self):
        partitions_init_info = psutil.disk_partitions()
        self.partitions = []
        for curr_partition in partitions_init_info:
            if curr_partition[2] != "":  # Ignore partition if there is no file system on it (ex: card readers)
                self.partitions.append(PartitionInfo(curr_partition[0]))

    # Get the names of all partitions
    def get_names(self):
        names = ""
        for partition in self.partitions:
            names += partition.device
        return names

    # Updates all the data.
    def refresh(self):
        for partition in self.partitions:
            partition.refresh()

    # Make points to send to influxdb.
    def make_points(self):
        json = []
        for partition in self.partitions:
            json.append(partition.make_points())
        return json

    def print(self):
        for partition in self.partitions:
            partition.print()


# Monitors the usage of 1 partitions.
class PartitionInfo:
    total_B = -1
    available_B = -1
    used_B = -1
    used_percent = -1

    assessment = ""
    smart_attributes = []

    def __init__(self, device_):
        self.device = device_
        # self.smart = pySMART.Device(self.device) todo <--- smart

        for partition in psutil.disk_partitions():
            if partition[0] == self.device:
                self.mount = partition[1]
                self.file_system = partition[2]
                self.options = partition[3]

        self.refresh()

    # Updates all the data.
    def refresh(self):
        self.refresh_used()
        # self.refresh_smart() todo <--- smart

    # Updates the used space data.
    def refresh_used(self):
        partitions_info = psutil.disk_usage(self.mount)
        self.total_B = partitions_info[0]
        self.available_B = partitions_info[2]
        self.used_B = partitions_info[1]
        self.used_percent = partitions_info[3]

    # Updates the SMART data.
    def refresh_smart(self):
        self.assessment = self.smart.assessment
        self.smart_attributes = self.smart.all_attributes()

    # Make points to send to parent class.
    def make_points(self):
        return {
            "measurement": "partition",
            "tags": {
                "machine": MACHINE_NAME,
                "partition": self.device.replace("\\", "")
            },
            "time": str(datetime.datetime.now().isoformat()),
            "fields": {
                "total": self.total_B,
                "available": self.available_B,
                "used": self.used_B,
                "used_percent": self.used_percent
            }
        }

    def print(self):
        print("Disk: %s    mount: %s  file system: %s  total: %s GB  used: %s GB" %
              (self.device, self.mount, self.file_system,
               round(self.total_B / 1000000000, 1), round(self.used_B / 1000000000, 1)))


# Monitors the i/o of all disks.
class AllDiskIOInfo(DeviceInfo):
    def __init__(self):
        disks_io_init_info = psutil.disk_io_counters(True)
        self.disks = [DiskIOInfo(disk_name)
                      for disk_name, disks_io_info
                      in disks_io_init_info.items()]

    def get_names(self):
        names = ""
        for disk in self.disks:
            names += disk.physical_drive
        return names

    # Updates all the data.
    def refresh(self):
        for disk in self.disks:
            disk.refresh()

    # Make points to send to influxdb.
    def make_points(self):
        json = []
        for disk in self.disks:
            json.append(disk.make_points())
        return json

    def print(self):
        for disk in self.disks:
            disk.print()


# Monitors the i/o of 1 disks.
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
                self.read_bytes = int(disk_io_info[2] / 8)
                self.read_count = disk_io_info[0]
                self.read_time = disk_io_info[4]
                self.write_bytes = int(disk_io_info[3] / 8)
                self.write_count = disk_io_info[1]
                self.write_time = disk_io_info[5]
                break

    # Make points to send to parent class.
    def make_points(self):
        return {
            "measurement": "disk_io",
            "tags": {
                "machine": MACHINE_NAME,
                "disk": self.physical_drive
            },
            "time": str(datetime.datetime.now().isoformat()),
            "fields": {
                "read_bytes": self.read_bytes,
                "read_count": self.read_count,
                "read_time": self.read_time,
                "write_bytes": self.write_bytes,
                "write_count": self.write_count,
                "write_time": self.write_time
            }
        }

    def print(self):
        print("Disk: %s    total read: %s GB  total written: %s GB" %
              (self.physical_drive, round(self.read_bytes / 1000000000, 1), round(self.write_bytes / 1000000000, 1)))


# Monitors the temperature of all devices.
class AllTempInfo(DeviceInfo):
    def __init__(self):
        self.available = False
        if hasattr(psutil, "sensors_temperatures"):  # Check if available
            sensors_init_info = psutil.sensors_temperatures()
            if sensors_init_info is not None:
                self.temp_devices = [TemperatureDevice(device_name)
                                     for device_name, sensors
                                     in sensors_init_info.items()]
                self.available = True

    def get_names(self):
        names = ""
        for device in self.temp_devices:
            names += device.clean_name
        return names

    # Updates all the data.
    def refresh(self):
        for device in self.temp_devices:
            device.refresh()

    # Make points to send to influxdb.
    def make_points(self):
        json = []
        for device in self.temp_devices:
            json.append(device.make_points())
        return json

    def print(self):
        for device in self.temp_devices:
            device.print()


# Monitors the temperature of all the sensors of 1 devices.
class TemperatureDevice:
    name_to_device = collections.defaultdict(str)
    # noinspection SpellCheckingInspection
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
                self.sensors = [TemperatureSensor(sensor_info[0], sensor_info[1], sensor_info[2], sensor_info[3])
                                for sensor_info
                                in sensors_info]
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

    # Make points to send to parent class.
    def make_points(self):
        # Basic temp info, for every device
        return {
            "measurement": "temp",
            "tags": {
                "machine": MACHINE_NAME,
                "device": self.clean_name
            },
            "time": str(datetime.datetime.now().isoformat()),
            "fields": {
                "average": self.average(),
                "highest": self.highest()[0],
                "lowest": self.lowest()[0],
                "high": self.high(),
                "critical": self.critical()
            }
        }

    def print(self):
        print("Device: %s    average temperature: %s C  %s sensor at critical temperature" %
              (self.clean_name, self.average(), self.critical()))


# Monitors the temperature of 1 sensor.
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

    def print(self):
        print("Sensor: %s    current temperature: %s C  high temperature: %s C  critical temperature: %s C" %
              (self.name, self.current, self.high, self.critical))


# Monitors the speed of all fans.
class AllFansInfo(DeviceInfo):
    def __init__(self):
        self.available = False
        if hasattr(psutil, "sensors_fans"):  # Check if available
            fans_init_info = psutil.sensors_fans()
            if fans_init_info is not None:
                self.fans = [FanInfo(device_name)
                             for device_name, sensors
                             in fans_init_info.items()]
                self.available = True

    def get_names(self):
        names = ""
        for fan in self.fans:
            names += fan.name
        return names

    # Updates all the data.
    def refresh(self):
        for fan in self.fans:
            fan.refresh()

    # Make points to send to influxdb.
    def make_points(self):
        json = []
        for fan in self.fans:
            json.append(fan.make_points())
        return json

    def print(self):
        for fan in self.fans:
            fan.print()


# Monitors the speed of 1 fans.
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

    # Make points to send to parent class.
    def make_points(self):
        return {
            "measurement": "fan",
            "tags": {
                "machine": MACHINE_NAME,
                "device": self.name
            },
            "time": str(datetime.datetime.now().isoformat()),
            "fields": {
                "rpm": self.rpm
            }
        }

    def print(self):
        print("Fan: %s    current speed: %s RPM" % (self.name, self.rpm))


# Monitors the battery information.
class BatteryInfo(DeviceInfo):
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

    # Make points to send to influxdb.
    def make_points(self):
        return [
            {
                "measurement": "battery",
                "tags": {
                    "machine": MACHINE_NAME
                },
                "time": str(datetime.datetime.now().isoformat()),
                "fields": {
                    "is_plugged": self.is_plugged,
                    "percent_left": self.percent_left,
                    "seconds_left": self.seconds_left
                }
            }
        ]

    def print(self):
        print("Battery:    plugged in: %s  percent left: %s  seconds left: %s" %
              (self.is_plugged, self.percent_left, self.seconds_left))
