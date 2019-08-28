'''
##############################################################################
Simple script to take in a list of addresses and identifiers as well as a list
of commands. The script uses the addresses and creates an SSH session with each
and then runs the supplied commands against them. The results are output to the
screen as well as a logfile in the same directory as the script.

Addresses spreadsheet input must have a title row and 2 colums. First column is
the identifier, second column is the IP address. All justified top left.

Commands are in a text standard text file, one line entered at a time.

Logfile output is called <host>-sshlog-<time stamp>.txt and is placed in the same
directory as the script.

Nathan Farrar - 8-Jul-2019
##############################################################################
'''

from netmiko import ConnectHandler
import select
import sys
import optparse
import csv
from time import gmtime, strftime, sleep
import time
import getpass

class logfile:

    def __init__(self, logfile_name, location):
        self.logfile_name = logfile_name
        self.logfile_location = location
        self.log_list = []

    def append_log(self, line):
        self.log_list.append(line)

    def write_log(self):
        f = open((self.logfile_location + self.logfile_name), 'w')
        for line in self.log_list:
            f.write(line + '\n')
        f.close()

def time_stamp():
    return str(strftime("%Y-%m-%d %H:%M:%S", time.localtime()))


def main():
    devices = []

    parser = optparse.OptionParser()

    parser.add_option('-a', '--addresses', action="store", dest="work_file", help="Excel sheet with addresses of devices", default='')
    parser.add_option('-c', '--commands', action="store", dest="command_file", help="Text file with commands", default='')

    options, args = parser.parse_args()

    print('Enter in password: ')
    get_password = getpass.getpass()

    work_file = options.work_file
    command_file = options.command_file

    # #open commands file and bring each line into a list and close file
    f = open(command_file, 'r')
    command_lines = f.readlines()
    command_lines = [x.strip() for x in command_lines]
    f.close()

    #create log object to write results to. The file has a timestamp in the name
    #log = logfile('sshlog-' + time_stamp() + '.txt', './')
    #log.append_log('-----Started: ' + time_stamp() + '-----')

    print('-----Started: ' + time_stamp() + '-----\n')

    #gather information from the spreadsheet. Iterate through each row
    #and fill a list with dictionaries of devices
    with open(work_file, mode='r', encoding='utf-8-sig') as f:
        device_instances = csv.DictReader(f)
        for row in device_instances:
            if row['password'] == 'none':
                devices.append({
                    'device_type': row['device_type'],
                    'host': row['host'],
                    'username': row['username'],
                    'password': get_password,
                    'secret': row['enable']
                })
            else:
                devices.append({
                    'device_type': row['device_type'],
                    'host': row['host'],
                    'username': row['username'],
                    'password': row['password'],
                    'secret': row['enable']
                })                

    for device in devices:
        current_address = device['host']
        print(device['username'])
        print(device['password'])


        #create log file object for each device connection
        log = logfile(f'{current_address}-sshlog-' + time_stamp() + '.txt', './')
        log.append_log('-----Started: ' + time_stamp() + '-----')

        print('\n')
        print('*'*60)
        print(f'Connecting to address {current_address}')

        log.append_log(time_stamp() + f' **********Connecting to address {current_address} **********')
        try:
            connection = ConnectHandler(**device)
            connection.enable()
            log.append_log(connection.find_prompt())
            print(connection.find_prompt())
            #output = connection.send_config_set(command_lines)

            for command in command_lines:
                print(command)
                output = connection.send_command(command)
                print(output)
                log.append_log(f' ********** {command} **********')
                log.append_log(output)

            connection.disconnect()
            log.append_log('----- Ended: ' + time_stamp() + '-----')
            log.write_log()
        except:
            #if an error is thrown, this is generic
            print(f'Unable to connect to {current_address}\n')
            log.append_log(time_stamp() + f' error connecting to {current_address}\n')

        #connection.disconnect()
    #clean up shop
    log.append_log('----- Ended: ' + time_stamp() + '-----')
    print('\n-----Ended: ' + time_stamp() + '-----')
    log.write_log()


if __name__ == '__main__':
    main()
