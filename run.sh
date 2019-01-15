
echo "Running..."

kill -2 $(pidof python)
sudo mn -c
ryu-manager ryu.app.simple_switch &
sudo python topology.py
kill -2 $(pidof python)

echo "Finished."
