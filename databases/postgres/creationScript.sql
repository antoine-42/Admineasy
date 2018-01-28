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
    net_ifaces          varchar(160),
    disk_names          varchar(160)
);

CREATE USER admineasy_client WITH PASSWORD '1337';
GRANT SELECT ON TABLE machines TO admineasy_client;
GRANT INSERT ON TABLE machines TO admineasy_client;
GRANT UPDATE  ON TABLE machines TO admineasy_client;

INSERT INTO machines VALUES ('desktop', 'windows_10...', 'windows', '10', 'antoine', '2018-01-28 15:30:15', 'i7 5820k', 12, 6, true, 1500, 4000, 16000, 16000, 'Ethernet', 'C:\\, D:\\');
INSERT INTO machines VALUES ('antoine_main', 'Windows-10-10.0.16299-SP0', 'Windows', '10', 'Antoin', '2018-01-28T02:31:57', 'Intel(R) Core(TM) i7-5820K CPU @ 3.30GHz', 6, 12, True, 0, 3300, 17070223360, 23198171136, 'EthernetEthernet 2Loopback Pseudo-Interface 1', 'C:D:');
