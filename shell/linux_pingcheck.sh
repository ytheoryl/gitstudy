#!/bin/bash
#timeout=30  # The number of seconds to wait for a response
timewait=5  # The number of seconds to interval for ping check
echo "Input all info below:"
read -p "Enter the target GNB IP: " input1
read -p "Enter the iperf command, e.g., iperf -c -u 1.2.3.4: " input2
read -p "Enter the timeout seconds of GNB: " input3
target_ip=$input1
iperfcmd=$input2
timeout=$input3

# Check if all inputs are valid
if [[ -z "$input1" || -z "$input2" || -z "$input3" ]]; then
    echo "Error: All inputs must be provided."
    exit 1
fi


###method 2, take user input as variables"
#target_ip="$1"
#iperfcmd="$3"
#timeout="$2"
:'
if [ $# -eq 0 ]; then
    echo "Usage: $0 [target_ip] [timeout] \"[iperf command]\""
    echo "Example:"
    echo "./checkgnb.sh 192.168.80.100 300 \"iperf -c -u 1.2.2.4\""
    exit 1
fi
'


#execution phase...
echo "1"
$iperfcmd
echo "2"
iperfpid=$(pgrep -f tightvnc)
echo $iperfpid

while true; do
    if ping -c 1 "$target_ip" > /dev/null; then
        echo "$target_ip is up! The next check will start after 5 seconds..."
        sleep $timewait
    else
        echo "$target_ip is down! The next check will start in $timewait seconds..."
        echo "$target_ip is up! The next check will start after 5 seconds..."
        sleep $timewait
    else
        echo "$target_ip is down! The next check will start in $timewait seconds..."
        sleep $timeout
        if ping -c 1 "$target_ip" > /dev/null; then
            echo "$target_ip is back up!"
        else
            echo "$target_ip is still down after $timeout seconds! Kill iperf session
 $iperfpid."
            kill $iperfpid
        fi
    fi
done
