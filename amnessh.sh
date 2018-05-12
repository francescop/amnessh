#!/bin/bash

SSH_CONFIG_FILE=$HOME/.ssh/config

awk '/^Host/ {print i++ " " $2}' $SSH_CONFIG_FILE

echo -n "server number (i + # for info): "
read server_number

if [[ "$server_number" == "i"* ]]; then 
  awk '/^Host/ {print i++ " " $2}' $SSH_CONFIG_FILE | \
    awk -v pattern=${server_number:1} '$0 ~ pattern {print $2}' | \
    xargs -i grep -A 4 "^Host {}$" $SSH_CONFIG_FILE
else
  awk '/^Host/ {print i++ " " $2}' $SSH_CONFIG_FILE | \
    awk -v pattern=$server_number '$0 ~ pattern {print $2}' | \
    xargs ssh
fi
