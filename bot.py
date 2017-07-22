#!/usr/bin/python

import socket
import json

team_name = "CHARLIETHEUNICORN"
# True if testing mode, False if production mode
test_switch = True
port = 25000

if test_switch:
    host_name = "test-exch-" + team_name
else:
    host_name = "production"

def connect():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host_name, port))
    return s.makefile('rw', 1)

def write_exchange(exchange, obj):
    json.dump(obj, exchange)
    exchange.write("\n")

def read_exchange(exchange):
    data = exchange.readline()
    if(data == ""):
        return None
    else:
        return json.loads(data)

def trade(exchange): 
    while True:
        data = read_exchange(exchange)
        print data

def main():
    exchange = connect()
    write_exchange(exchange, {"type": "hello", "team": team_name})
    hello_exchange = read_exchange(exchange)
    trade(exchange)

if __name__ == '__main__':
    while True:
        main()
