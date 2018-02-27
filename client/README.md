# Admineasy: client
Ce répertoire contient tout le code utilisé par le client
## harvester/
### databases.py
Connection et communication avec les bases de données.
### devices.py
Collecte d'informations.
### harvester.py
Fichier principal.
### settings.json
Fichier de configuration.
## installer/
### installer.py
Script qui met en place le client comme un service avec NSSM (Windows) pour qu'il soit lancé au démarrage.
## uninstaller/
### uninstaller.py
Script qui supprime le service.
### uninstall_script_win.ps1
Script powershell qui
### grafana.json
backup d'une config grafana qui permet de visualiser les données récupérées par le client.
### harvester.nsi
Script NSIS de création de l'installeur. L'installeur lance le script d'installation quand il a fini de copier les fichiers, et crée un désinstalleur qui lance le script de désinstallation.
### harvester.spec, setup.spec, uninstaller.spec
Scripts pyinstaller pour "freezer" le programme et obtenir des executables qui n'ont pas besoin d'une installation de Python ou des librairies.

Pyinstaller vas fournir des executables en fonction de la plateforme ou il est lancé: sur windows, il vas fournir des .exe.

Il est théoriquement possible de faire 1 script et de faire utiliser les meme ressources pour tout les programmes, mais ca marche pas.
### nssm.exe
Utilisé pour installer harvester en tant que service sur Windows.