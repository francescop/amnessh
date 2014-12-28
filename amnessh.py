#!/usr/bin/env python

import os
import ConfigParser
import sys
import getopt

config = ConfigParser.RawConfigParser() # global configurator
config_filepath = os.getenv("HOME") + "/.amnessh.cfg" # settings' file path
counter = 0 # server number counter
servers = [] # server list

# print usage instrunctions
def usage():
    print "-a, --add\n\t add server"
    print "-r, --remove\n\t remove server"
    print "-l, --help\n\t show server list"
    print "-h, --help\n\t this screen"

# get the number of the server to connect to
def ask_server():
    num = int(raw_input("server number: "))
    if num > counter:
        print "no server" # number insterted out of server list
    else:
        command = servers[num-1][1] # get the command to connetc to the server. num-1 because an array starts from 0 but we are showing numbers from 1
        os.system(command) # execute the command

# show the server list
def show_server_list():
    global counter # to edit the counter
    for server in servers:
        # for each server in the array increment the counter and show the command
        counter += 1
        if counter > 0:
            print counter,") ",server[0],"\t",server[1]
    if not counter > 0: # obviously if the counter is 0 there are no servers inserted yet
        print "no servers"
        sys.exit()

# add the server to the list
def add_server():
    name = raw_input("insert server hostname: ") # get the name
    command = raw_input("insert command to connect to server (ssh root@....): ") # get the command
    config.set('Servers', name, command) # add the server to the configuration
    with open(config_filepath, 'wb') as configfile: # write it to the configuration file
        config.write(configfile)
        configfile.close()
    sys.exit()

# add the server from the list
def remove_server():
    num = int(raw_input("insert server you want delete: ")) # get the number in the list
    if num > counter:
        print "no server" # number insterted out of server list
    else:
        config.remove_option('Servers', servers[num-1][0]) # remove the server to the configuration. num-1 because an array starts from 0 but we are showing numbers from 1
        print "removing", servers[num-1][0]
        with open(config_filepath, 'wb') as configfile: # write the changes to the configuration file
            config.write(configfile)
            configfile.close()
    sys.exit()


def main():
    if not os.path.isfile(config_filepath): # if there's no setttings file create it
        config.add_section('Servers')
        with open(config_filepath, 'wb') as configfile:
            config.write(configfile)
            configfile.close()
    else: # otherwise read it
        config.read(config_filepath)
        global servers
        servers = config.items('Servers') # put all the server listed into an array

    try:
        opts, args = getopt.getopt(sys.argv[1:], "arhl", ["help", "list", "add", "remove"]) # set the valid options
    except getopt.GetoptError: # fallback if option inserted is not valid
        usage()
        sys.exit(2)

    if opts:
        for opt, arg in opts:
            if opt in ('-a', '--add'):
                add_server()
            elif opt in ('-r', '--remove'):
                show_server_list()
                remove_server()
            elif opt in ('-h', '--help'):
                usage()
                sys.exit()
            elif opt in ('-l', '--list'):
                show_server_list()
                sys.exit()
            else:
                usage()
                sys.exit()

    else:
        show_server_list()
        ask_server()

if __name__ == "__main__":
    main()
