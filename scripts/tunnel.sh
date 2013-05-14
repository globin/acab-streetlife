#!/bin/bash

SERVER_IP=valhalla.fs.tum.de
SERVER_USER=hertle

PORTS="5008 6002"
PORTS="5008"

PID_FILE="/tmp/led-ssh-tunnel"

# Command line parameter
case "$1" in
"start")
    do_stop=1
    do_start=1
    ;;
"stop")
    do_stop=1
    do_start=0
    ;;
*)
    echo "$(basename $0) start|stop"
    exit
    ;;
esac

# Stop
if [ "$do_stop" == "1" ] ; then
    for p in $PORTS ; do
        if [ -f "$PID_FILE_$p" ] ; then
            echo "Kill tunnel on port $p"

            start-stop-daemon --pidfile "$PID_FILE_$p" --stop

            rm -f "$PID_FILE_$p"
        fi
    done
fi

if [ "$do_start" == "1" ] ; then
    for p in $PORTS ; do
        echo "Start tunnel on port $p"

        start-stop-daemon --pidfile "$PID_FILE_$p" --make-pidfile --exec /usr/bin/ssh --start -- -N $SERVER_USER@$SERVER_IP -L $p:meinserver:$p &
    done
fi
