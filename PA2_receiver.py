#!/usr/bin/env python3
# Last updated: Oct, 2021

import sys
import time
import socket
import datetime 
from checksum import checksum, checksum_verifier
import re

CONNECTION_TIMEOUT = 60 # timeout when the receiver cannot find the sender within 60 seconds
FIRST_NAME = "AADITYA"
LAST_NAME = "VIKRAM"
PACKETPATTERN_OUT = r"([0-9]*)\s+([0-9]*)\s+(.{20})\s+([0-9]{5})"

p_out_regex = re.compile(PACKETPATTERN_OUT)
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
        # dataSock.sendall(bytes("  0                      00720", "utf-8"))
        with dataSock:
            # checking
            ack_bool = False
            seq_bool = False

            # this part should be in a loop
            #TESTING: for loop recieves 10 packets
            for i in range(10):    
                buf = dataSock.recv(30)
                print(buf.decode("UTF-8"))
                packetString = buf.decode("UTF-8")
                print(f"client SAYS: {packetString}")
                match: re.match = re.match(p_out_regex, packetString)
                print(match[1])

                if not checksum_verifier(packetString) or match[2] == (0 if seq_bool else 1):
                    if ack_bool:
                        dataSock.sendall(bytes("  1                      00721", "utf-8"))
                    else:
                        dataSock.sendall(bytes("  0                      00720", "utf-8"))
                    
                    buf = dataSock.recv(30)
                    print(buf.decode("UTF-8"))
                    packetString = buf.decode("UTF-8")
                    print(f"RETRYING --- client SAYS: {packetString}")
                    match: re.match = re.match(p_out_regex, packetString)

                # invert bools and start over
                ack_bool = not ack_bool
                seq_bool = not seq_bool            
                


        # if (datastring[0] != "OK"):
        #     #error case
        #     pass








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
