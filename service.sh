startProcess=$1

if [ $startProcess = "start" ]; then
    echo "Starting process"
    echo "start" > ./start_process.txt
    python3 ./main.py
    # Start process
elif [ $startProcess = "stop" ]; then
    echo "Stopping process"
    echo "stop" > ./start_process.txt
    # Stop process
else
    echo "Invalid command"
    echo "Usage ./service.sh start|stop"
fi
