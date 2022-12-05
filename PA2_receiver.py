#!/usr/bin/env python3
# Last updated: Oct, 2021

import random
import sys
import time
import socket
import datetime 
from checksum import checksum, checksum_verifier
import re

CONNECTION_TIMEOUT = 60 # timeout when the receiver cannot find the sender within 60 seconds
FIRST_NAME = "AADITYA"
LAST_NAME = "VIKRAM"
PACKETPATTERN= r"([0-9])\s([0-9])\s([\S\s]{20})\s([0-9]{5})"

p_regex = re.compile(PACKETPATTERN)
def start_receiver(server_ip, server_port, connection_ID, loss_rate=0.0, corrupt_rate=0.0, max_delay=0.0):
    """
     This function runs the receiver, connnect to the server, and receiver file from the sender.
     The function will print the checksum of the received file at the end. 
     The checksum is expected to be the same as the checksum that the sender prints at the end.

     Input: 
        server_ip - IP of the server (String)
        server_port - Port to connect on the server (int)
        connection_ID - your sender and receiver should specify the same connection ID (String)
        loss_rate - the probabilities that a message will be lost (float - default is 0, the value should be between 0 to 1)
        corrupt_rate - the probabilities that a message will be corrupted (float - default is 0, the value should be between 0 to 1)
        max_delay - maximum delay for your packet at the server (int - default is 0, the value should be between 0 to 5)

     Output: 
        checksum_val - the checksum value of the file sent (String that always has 5 digits)
    """

    print("Student name: {} {}".format(FIRST_NAME, LAST_NAME))
    print("Start running receiver: {}".format(datetime.datetime.now()))

    checksum_val = "00000"

    ##### START YOUR IMPLEMENTATION HERE #####
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as clientSock:

        # clientSock.connect((server_ip, server_port))

        # TEMPORARY: this is a "server" for localhost purposes
        clientSock.bind((server_ip, server_port))
    
        # HELLO R <loss_rate> <corrupt_rate> <max_delay> <ID>
        # read page 5-6 for debugging (connection_ID in use etc.)
        hello_msg = "HELLO R {} {} {} {}".format(loss_rate, corrupt_rate, max_delay, connection_ID)
        print(hello_msg)

        
        # TEMPORARY: no identification needed: this is the server...we're skipping the manual handshake

        # # NOTE: <loss_rate> <corrupt_rate> are float values in the range [0.0, 1.0]
          # clientSock.sendall(bytes(hello_msg, "UTF-8"))

        # TEMPORARY: no need for a data_socket...again it's not a server
        clientSock.listen()
        dataSock, ret_addr = clientSock.accept()
        with dataSock:
            with open("declaration_server.txt", "w") as out:
                # checking
                ack_bool = False        
                seq_bool = False

                while True:
                    # recieve the data packet

                    # loss would be ju


                    buf = dataSock.recv(30)
                    packetString = buf.decode("UTF-8")
                    if (packetString == ""):
                        break

                    print(f"CLIENT says: {packetString}")
                    match: re.Match = re.match(p_regex, packetString)
                    seq_bool = True if match[1] == '1' else False
                    
                    # pAK
                    if seq_bool == ack_bool and checksum_verifier(packetString):
                        out.write(match[3])
                        ack_bool = not ack_bool
                    
                    
                    tmp = 1 if seq_bool else 0
                    chksum = checksum(f"  {tmp}                      ")
                    # checking if corruption is handled properly
                    chksum = '10001' if random.randint(0, 10) > 7 else chksum
                    dataSock.sendall(bytes(f"  {tmp}                      {chksum}", "utf-8"))

    ##### END YOUR IMPLEMENTATION HERE #####

    print("Finish running receiver: {}".format(datetime.datetime.now()))

    # PRINT STATISTICS
    # PLEASE DON'T ADD ANY ADDITIONAL PRINT() AFTER THIS LINE
    print("File checksum: {}".format(checksum_val))

    return checksum_val

 
if __name__ == '__main__':
    # CHECK INPUT ARGUMENTS
    # if len(sys.argv) != 7:
    #     print("Expected \"python PA2_receiver.py <server_ip> <server_port> <connection_id> <loss_rate> <corrupt_rate> <max_delay>\"")
    #     exit()

    # server_ip, server_port, connection_ID, loss_rate, corrupt_rate, max_delay = sys.argv[1:]

    # TEMPORARY RESOLUTION FOR LOCALHOST
    server_ip, server_port, connection_ID, loss_rate, corrupt_rate, max_delay \
    =  "127.0.0.1", 1025, 6464, 0.0, 0.0, "declaration.txt"
    
    
    # START RECEIVER
    start_receiver(server_ip, int(server_port), connection_ID, loss_rate, corrupt_rate, max_delay)
