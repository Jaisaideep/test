#!/bin/sh

cd /apps/opt/application/looker
# set your java memory- there should be over 1.5G of system memory 
# left to run the OS
MEM=$(cat /proc/meminfo | grep MemTotal | awk '{print $2}')
JM=$(expr $MEM \* 6 / 10)
JAVAMEM="46000m"
METAMEM="1000m"

# Extra Java startup args and Looker startup args.  These can also be set in
# a file named lookerstart.cfg
JMXARGS="-Dcom.sun.akuma.jvmarg.com.sun.management.jmxremote -Dcom.sun.akuma.jvmarg.com.sun.management.jmxremote.port=9910 -Dcom.sun.akuma.jvmarg.com.sun.management.jmxremote.ssl=false -Dcom.sun.akuma.jvmarg.com.sun.management.jmxremote.local.only=false -Dcom.sun.akuma.jvmarg.com.sun.management.jmxremote.authenticate=true -Dcom.sun.akuma.jvmarg.com.sun.management.jmxremote.access.file=${HOME}/.lookerjmx/jmxremote.access -Dcom.sun.akuma.jvmarg.com.sun.management.jmxremote.password.file=${HOME}/.lookerjmx/jmxremote.password"

# to set up JMX monitoring, add JMXARGS to JAVAARGS
JAVAARGS=""
LOOKERARGS=""

# check for a lookerstart.cfg file to set JAVAARGS and LOOKERARGS
if [ -r ./lookerstart.cfg ]; then
  . ./lookerstart.cfg
fi

# check if --no-ssl is specified in LOOKERARGS and set protocol accordingly
PROTOCOL=""

export LKR_MASTER_KEY_FILE=/home/looker/looker/looker_key.txt

echo "${LOOKERARGS}" | grep -q "\-\-no\-ssl"
if [ $? -eq 0 ] 
then
        PROTOCOL='http'
else
        PROTOCOL='https'
fi
LOOKERPORT=${LOOKERPORT:-"9999"}

start() {
    if [ -e .deploying ]; then
        echo "Startup suppressed: ${PWD}/.deploying file exists.  Remove .deploying file to allow startup"
        exit 1
    fi

    LOCKFILE=.starting
    if [ -e ${LOCKFILE} ] && kill -0 `cat ${LOCKFILE}`; then
        echo "Startup suppressed: ${LOCKFILE} contains running pid, startup script is already running"
        exit 1
    fi

    # make sure the lockfile is removed when we exit and then claim it
    trap "rm -f ${LOCKFILE}; exit" INT TERM EXIT
    echo $$ > ${LOCKFILE}

    fixcrypt
    java \
  -XX:+UseG1GC -XX:MaxGCPauseMillis=2000 -XX:MaxMetaspaceSize=$METAMEM \
  -Xms$JAVAMEM -Xmx$JAVAMEM \
  -verbose:gc -XX:+PrintGCDetails -XX:+PrintGCTimeStamps \
  -Xloggc:/tmp/gc.log  ${JAVAARGS} \
  -javaagent:/apps/opt/application/newrelic/newrelic.jar -jar looker.jar start ${LOOKERARGS}

    if [ -x ./tunnel ]; then
       ./tunnel start
    fi

    rm -f ${LOCKFILE}
}

stop() {
    if [ -e .tmp/looker.pid ]; then
        pid=$(cat .tmp/looker.pid)
        if ps -p $pid > /dev/null; then
            # Process exists, so attempt to stop it
            if [ -f .status_server_token ] && [ -x /usr/bin/curl ]; then
                state="running"
                token=$(cat .status_server_token)
                request="control/stop?token=${token}"
                timeout 20 curl -m 10 -ks ${PROTOCOL}://127.0.0.1:${LOOKERPORT}/${request} > /dev/null 2>&1
                ECODE=$?
                [ $ECODE -eq 7 ] && state="stopped"
                if [ $ECODE -gt 7 ] ; then
                    kill $pid
                fi
                for i in {1..30}; do
                    timeout 20 curl -m 5 -ks ${PROTOCOL}://127.0.0.1:${LOOKERPORT}/alive > /dev/null 2>&1
                    ECODE=$?
                    if [ $ECODE -eq 7 ]; then
                        state="stopped"
                        break
                    fi
                    if [ $ECODE -gt 7 ] ; then
                        kill -9 $pid
                    fi
                    sleep 1
                done
                if [ "${state}" = "running" ]; then
                    echo "Force Stop Looker Web Application"
                    kill $pid
                    kill -0 $pid && kill -9 $pid
                fi
            else
                timeout 20 java -jar looker.jar stop
                if [ $? -ne 0 ]; then
                    kill -9 $pid
                fi
            fi
        else
            echo "Looker process with PID $pid is not running."
        fi
    else
        echo "Looker PID file does not exist."
    fi
}

fixcrypt() {
    CRYPTEXIST=$(/sbin/ldconfig -p | grep -c '\slibcrypt.so\s')

    if [ $CRYPTEXIST -eq 0 ]; then
        if [ ! -d .tmp ]; then
            mkdir .tmp
        fi
        CRYPTLN=$(/sbin/ldconfig -p | grep '\slibcrypt\.so\.[[:digit:]]' | awk '{print $(NF)}')
        ln -s -f $CRYPTLN $(pwd)/.tmp/libcrypt.so
        export LD_LIBRARY_PATH=$(pwd)/.tmp/:$LD_LIBRARY_PATH
    fi
}

case "$1" in
  start)
    start
        ;;
  stop)
    stop
        ;;
  restart)
        echo "Restarting Looker Web Application" "looker"
        stop
        sleep 3
        start
        ;;
  status)
        curl -ks ${PROTOCOL}://127.0.0.1:${LOOKERPORT}/alive > /dev/null 2>&1
        if [ $? -eq 7 ]; then
          echo "Status:Looker Web Application stopped"
          exit 7
        else
          echo "Status:Looker Web Application running"
          exit 0
        fi
        ;;
  *)
        java -jar looker.jar $*
        ;;
esac

exit 0