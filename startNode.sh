#!/bin/bash
echo "Lancement des serveurs js"

#Chemins d'accès
node="./n/bin/node"
log="./logs_node/"

#Paramétrage des fichiers de logs
log_serveur="$log/serveurDB.log"
log_ping="$log/pingPlage.log"
log_influx="$log/webapp.log"

#Lancement des serveurs
$node serveur.js > $log_serveur &
$node pingPlage.js > $log_ping &
$node influx_web/webapp.js > $log_influx &

echo "Les serveurs sont opérationnels"
