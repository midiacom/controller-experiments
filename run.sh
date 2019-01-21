
echo "Running..."

pkill ryu-manager
sudo mn -c &> /dev/null
ryu-manager --verbose ryu.app.simple_switch &> logs/ryu.log 2>&1 &
# sudo python topology.py > logs/mininet.log 2>&1
sudo python topology.py
pkill ryu-manager

echo "Finished."
