import psycopg2  # Communication with PostgreSQL.
import influxdb  # Communication with influxdb.


# Handles the connection with PostgreSQL
class PostgreSQLconn:
    machine = None
    users = None
    cpu = None
    ram = None
    swap = None
    net_ifaces = None
    disks = None

    postgres_connection = None
    postgres_cursor = None

    def __init__(self, options):
        self.host = options["host"]
        self.database = options["database"]
        self.login = options["login"]
        self.password = options["password"]

    # Connect to the database
    def connect(self):
        self.postgres_connection = psycopg2.connect(
            host=self.host, database=self.database, user=self.login, password=self.password
        )
        self.postgres_cursor = self.postgres_connection.cursor()

    # disconnect from the database
    def disconnect(self):
        self.postgres_connection.close()

    # Get the measurements
    def get_measurements(self, measurements):
        self.machine = measurements[0]
        self.users = measurements[1]
        self.cpu = measurements[2]
        self.ram = measurements[3]
        self.swap = measurements[4]
        self.net_ifaces = measurements[5]
        self.disks = measurements[6]

    # Check if this computer exists, then update or create new entry
    def send_data(self):
        if self.check_exists():
            self.update_db()
        else:
            self.create_entry()

    # Check if this computer exists
    def check_exists(self):
        self.postgres_cursor.execute("""SELECT * FROM machines WHERE name='%s' AND os_complete='%s';"""
                                     % (self.machine.name, self.machine.os_full))
        result = self.postgres_cursor.fetchall()
        if len(result) > 0:
            return True
        return False

    # Add this computer to the database
    def create_entry(self):
        self.postgres_cursor.execute(
            """INSERT INTO machines VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', %d, %d, '%s', %d, %d, %d, %d, '%s', '%s', '%s');"""
            % (
                self.machine.name, self.machine.os_full, self.machine.os_name, self.machine.os_version,
                self.users.users[0].name, self.users.users[0].start, self.cpu.name, self.cpu.physical_cores,
                self.cpu.logical_cores, self.cpu.hyper_threading, self.cpu.freq_min_mhz, self.cpu.freq_max_mhz,
                self.ram.total_B / 1000000, self.swap.total_B / 1000000, self.net_ifaces.localIP,
                self.net_ifaces.get_names(), self.disks.get_names()
               )
        )
        self.postgres_connection.commit()

    # Update the data on this computer
    def update_db(self):
        self.postgres_cursor.execute(
            """UPDATE machines SET 
                   user_name='%s', connection_time='%s', cpu_name='%s', cpu_cores=%d, cpu_threads=%d, 
                   cpu_hyperthreading='%s', cpu_freqmin=%d, cpu_freqmax=%d, ram_total=%d, swap_total=%d, local_ip='%s', 
                   net_ifaces='%s', disk_names='%s'
                WHERE name='%s' AND os_complete='%s';"""
            % (
                self.users.users[0].name, self.users.users[0].start, self.cpu.name, self.cpu.physical_cores,
                self.cpu.logical_cores, self.cpu.hyper_threading, self.cpu.freq_min_mhz, self.cpu.freq_max_mhz,
                self.ram.total_B / 1000000, self.swap.total_B / 1000000, self.net_ifaces.localIP,
                self.net_ifaces.get_names(), self.disks.get_names(),
                self.machine.name, self.machine.os_full
               )
        )
        self.postgres_connection.commit()


# Handles the connection with influxDB
class InfluxConn:
    def __init__(self, options):
        self.influxdb_connection = influxdb.InfluxDBClient(
            host=options["host"], database=options["database"], username=options["login"], password=options["password"])

    # Sends the points in json to influx
    def write_points(self, json):
        return self.influxdb_connection.write_points(json)
