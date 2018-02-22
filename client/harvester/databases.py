import psycopg2  # Communication with PostgreSQL.
import influxdb  # Communication with influxdb.


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

    def __init__(self):
        self.get_measurements()

        try:
            self.connect()
        except psycopg2.OperationalError as err:
            print("Can't connect to PostgreSQL database")
            print(err)
            return

        if self.check_exists():
            self.update_db()
        else:
            self.create_entry()

    # Get the measurements
    def get_measurements(self, measurements):
        self.machine = measurements[0]
        self.users = measurements[1]

        #users_init_info = psutil.users()
        #self.users = []
        #for user_init_info in users_init_info:
        #    self.users.append(UserInfo(user_init_info[0]))

        self.cpu = measurements[2]
        self.ram = measurements[3]
        self.swap = measurements[4]
        self.net_ifaces = measurements[5]
        self.disks = measurements[6]

    # Connect to the database
    def connect(self):
        self.postgres_connection = psycopg2.connect(
            host="10.8.0.1", database="admineasy", user="admineasy_client", password="1337"
        )
        self.postgres_cursor = self.postgres_connection.cursor()

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
                self.users[0].name, self.users[0].start, self.cpu.name, self.cpu.physical_cores, self.cpu.logical_cores,
                self.cpu.hyper_threading, self.cpu.freq_min_mhz, self.cpu.freq_max_mhz,
                self.ram.total_B / 1000000, self.swap.total_B / 1000000, self.net_ifaces.localIP, self.net_ifaces.get_names(), self.disks.get_names()
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
                self.users[0].name, self.users[0].start, self.cpu.name, self.cpu.physical_cores, self.cpu.logical_cores,
                self.cpu.hyper_threading, self.cpu.freq_min_mhz, self.cpu.freq_max_mhz,
                self.ram.total_B / 1000000, self.swap.total_B / 1000000, self.net_ifaces.localIP,
                self.net_ifaces.get_names(), self.disks.get_names(),
                self.machine.name, self.machine.os_full
               )
        )
        self.postgres_connection.commit()


class InfluxConn:
    def __init__(self):
        self.influxdb_connection = influxdb.InfluxDBClient(
            host="10.8.0.1", database="admineasy", username="admineasy-client", password="1337")

    def write_points(self, json):
        return self.influxdb_connection.write_points(json)
