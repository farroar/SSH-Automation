# SSH-Automation
Script used to push SSH commands to devices

It takes in a .csv file and a plain text file. Uses the csv file to build a list of devices to connect to and then parses the text file for commands to send to each device.

This script uses the paramiko library.

It also creates a log file for each device it connects to and places them into the same directory where the script is run

Basic usage:

SSHCommands-v2.py -a (hosts file) -c (command file)

check out ktbyers and netmiko documentation for details on how the SSH connections and hosts files work
