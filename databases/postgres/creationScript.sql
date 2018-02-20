CREATE DATABASE admineasy WITH ENCODING = UTF8;

CREATE TABLE machines (
    name                varchar(80),
    os_complete         varchar(80),
    os_simple           varchar(80),
    os_version          varchar(80),
    user_name           varchar(80),
    connection_time     timestamp,
    cpu_name            varchar(80),
    cpu_cores           int,
    cpu_threads         int,
    cpu_hyperthreading  bool,
    cpu_freqmin         int,
    cpu_freqmax         int,
    ram_total           int,
    swap_total          int,
    local_ip            varchar(80),
    net_ifaces          varchar(160),
    disk_names          varchar(160)
);

CREATE UNIQUE INDEX idx_machines on machines(name, os_complete);

CREATE USER admineasy_client WITH PASSWORD '1337';
GRANT SELECT ON TABLE machines TO admineasy_client;
GRANT INSERT ON TABLE machines TO admineasy_client;
GRANT UPDATE  ON TABLE machines TO admineasy_client;

INSERT INTO machines VALUES ('antoine_main', 'Windows-10-10.0.16299-SP0', 'Windows', '10', 'Antoin', '2018-01-28T02:31:57', 'Intel(R) Core(TM) i7-5820K CPU @ 3.30GHz', 6, 12, True, 0, 3300, 17070, 23198, '192.168.1.42', 'EthernetEthernet 2Loopback Pseudo-Interface 1', 'C:D:');

UPDATE machines SET user_name='Antoine', connection_time='2018-02-20T15:42:57', cpu_name='Intel(R) Core(TM) i7-5820K CPU @ 3.30GHz', cpu_cores=6, cpu_threads=12, cpu_hyperthreading='True', cpu_freqmin=0, cpu_freqmax=3300, ram_total=17070, swap_total=23198, local_ip='192.168.1.42', net_ifaces='EthernetEthernet 2Loopback Pseudo-Interface 1', disk_names='C:D:' WHERE name='antoine_main' AND os_complete='Windows-10-10.0.16299-SP0';
