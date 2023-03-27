# System-Resource-Monitor
System Resource Monitor is a lightweight command-line utility that monitors resource usage of a system. It provides a convenient way to display key system resource metrics, including CPU usage, memory usage, disk space, and the top running processes.

To obtain system performance data, the script uses the 'psutil' module. The utility runs continuously and refreshes the data every 3 seconds, making it a useful tool for monitoring the system over time. The top processes that are using the most CPU resources are also listed, making it easy to identify processes that may be causing the system to slow down or become unresponsive.

# Usage
To run the script, simply run the main.py file in a terminal window.

# Dependencies
This script requires the 'psutil' library to get CPU usage, memory usage, and disk usage which can be installed using the following command:
~~~ 
pip install psutil
~~~
