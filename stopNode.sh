#!/bin/bash

pid=`ps -u | grep "node" | cut -d " " -f 5`

kill -9 $pid 2> /dev/null

echo "Les serveurs node ont été arrêtés"
