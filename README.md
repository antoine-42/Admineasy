# Admineasy

Admineasy est une application de surveillance de ressources système. Le client, harvester, est installé sur des ordinateurs et envoie les informations d'utilisation a une base de données InfluxDB et PostgreSQL. Un serveur web affiche ces informations proprement.

## Installation

L'installeur vas copier les fichiers, et mettre en place un service qui vas lancer le programme a chaque démarrage. Changez la configuration dans [répertoire d'installation]\harvester\harvester\settings.json si besoin.

### Linux

Telecharger [harvester-setup.run](https://github.com/antoine-42/admineasy/releases).

`sudo ./harvester-setup.run --target /opt/admineasy`

### Windows

Telecharger [admineasy.exe](https://github.com/antoine-42/admineasy/releases) et lancer le en tant qu'administrateur.

## Harvester

### Librairies Python

- [psutil](http://psutil.readthedocs.io/en/latest/)
- [py-cpuinfo](https://github.com/workhorsy/py-cpuinfo)
- [pySMART](https://pypi.python.org/pypi/pySMART)
- [influxdb](https://influxdb-python.readthedocs.io/)
- [psycopg2](https://pypi.python.org/pypi/psycopg2/)
- [PyInstaller](http://www.pyinstaller.org/) pour faire un executable standalone.

### Autres logiciels

- [Makeself](http://makeself.io/) pour faire un installeur sur Linux.
- [NSIS](http://nsis.sourceforge.net/Main_Page) pour faire un installeur sur Windows.
- [NSSM](http://nssm.cc/) pour installer le programme comme un service sur windows.
- Base de données [InfluxDB](https://docs.influxdata.com/influxdb/v1.3/introduction/getting_started/) et [PostgreSQL](https://www.postgresql.org/).
- [Grafana](http://docs.grafana.org/) pour faire des graphes jolis facilement. J'ai mis un backup de ma config pour une machine dans grafana.json.
