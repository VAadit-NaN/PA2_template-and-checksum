#!/usr/bin/env python3
# Last updated: Oct, 2021

import sys
import time
import socket
import datetime 
from checksum import checksum, checksum_verifier

CONNECTION_TIMEOUT = 60 # timeout when the receiver cannot find the sender within 60 seconds
FIRST_NAME = "AADITYA"
LAST_NAME = "VIKRAM"

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
        clientSock.connect((server_ip, server_port))
    
        # HELLO R <loss_rate> <corrupt_rate> <max_delay> <ID>
        # read page 5-6 for debugging (connection_ID in use etc.)
        hello_msg = "HELLO R {} {} {} {}".format(loss_rate, corrupt_rate, max_delay, connection_ID)
        print(hello_msg)

        # NOTE: <loss_rate> <corrupt_rate> are float values in the range [0.0, 1.0]
        clientSock.sendall(bytes(hello_msg, "UTF-8"))

        # 32 is arbitrary. May need to be bigger
        data = clientSock.recv(32)
        print(data.decode("UTF-8").strip())
        datastring = data.decode("UTF-8").strip().split()

        if (datastring[0] != "OK"):
            #error case
            pass







    ##### END YOUR IMPLEMENTATION HERE #####

    print("Finish running receiver: {}".format(datetime.datetime.now()))

    # PRINT STATISTICS
    # PLEASE DON'T ADD ANY ADDITIONAL PRINT() AFTER THIS LINE
    print("File checksum: {}".format(checksum_val))

    return checksum_val

 
if __name__ == '__main__':
    # CHECK INPUT ARGUMENTS
    if len(sys.argv) != 7:
        print("Expected \"python PA2_receiver.py <server_ip> <server_port> <connection_id> <loss_rate> <corrupt_rate> <max_delay>\"")
        exit()
    server_ip, server_port, connection_ID, loss_rate, corrupt_rate, max_delay = sys.argv[1:]
    # START RECEIVER
    start_receiver(server_ip, int(server_port), connection_ID, loss_rate, corrupt_rate, max_delay)
