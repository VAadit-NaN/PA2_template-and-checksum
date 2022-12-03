#!/usr/bin/env python3
# Last updated: Oct, 2021

import random
import sys
import socket
import datetime
from checksum import checksum, checksum_verifier
import re

CONNECTION_TIMEOUT = 60 # timeout when the sender cannot find the receiver within 60 seconds
FIRST_NAME = "FIRSTNAME"
LAST_NAME = "LASTNAME"
PACKETPATTERN = r"([0-9]*)\s+([0-9]*)\s+(.{20})\s+([0-9]{5})"

p_regex = re.compile(PACKETPATTERN)

def start_sender(server_ip, server_port, connection_ID, loss_rate=0, corrupt_rate=0, max_delay=0, transmission_timeout=60, filename="declaration.txt"):
    """
     This function runs the sender, connnect to the server, and send a file to the receiver.
     The function will print the checksum, number of packet sent/recv/corrupt recv/timeout at the end. 
     The checksum is expected to be the same as the checksum that the receiver prints at theend.

     Input: 
        server_ip - IP of the server (String)
        server_port - Port to connect on the server (int)
        connection_ID - your sender and receiver should specify the same connection ID (String)
        loss_rate - the probabilities that a message will be lost (float - default is 0, the value should be between 0 to 1)
        corrupt_rate - the probabilities that a message will be corrupted (float - default is 0, the value should be between 0 to 1)
        max_delay - maximum delay for your packet at the server (int - default is 0, the value should be between 0 to 5)
        tranmission_timeout - waiting time until the sender resends the packet again (int - default is 60 seconds and cannot be 0)
        filename - the path + filename to send (String)

     Output: 
        checksum_val - the checksum value of the file sent (String that always has 5 digits)
        total_packet_sent - the total number of packet sent (int)
        total_packet_recv - the total number of packet received, including corrupted (int)
        total_corrupted_pkt_recv - the total number of corrupted packet receieved (int)
        total_timeout - the total number of timeout (int)

    """

    print("Student name: {} {}".format(FIRST_NAME, LAST_NAME))
    print("Start running sender: {}".format(datetime.datetime.now()))

    checksum_val = "00000"
    total_packet_sent = 0
    total_packet_recv = 0
    total_corrupted_pkt_recv = 0
    total_timeout =  0

    print("Connecting to server: {}, {}, {}".format(server_ip, server_port, connection_ID))

    ##### START YOUR IMPLEMENTATION HERE #####

    # create a TCP socket and connect to port 20500 at gaia.cs.umass.edu
    # (ASSUMING these are server_ip and server_port)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as clientSock:
        clientSock.connect((server_ip, server_port))
    
        # HELLO S <loss_rate> <corrupt_rate> <max_delay> <ID>
        # read page 5-6 for debugging (connection_ID in use etc.)
        hello_msg = f"HELLO S {loss_rate} {corrupt_rate} {max_delay} {connection_ID}"
        print(hello_msg)

        # TEMPORARY: no need for manual handshake...this is localhost
            # NOTE: <loss_rate> <corrupt_rate> are float values in the range [0.0, 1.0]
            # clientSock.sendall(bytes(hello_msg, "UTF-8"))

            # # 32 is arbitrary. May need to be bigger
            # data = clientSock.recv(32)
            # print(data.decode("UTF-8").strip())
            # datastring = data.decode("UTF-8").strip().split()
            # if (datastring[0] != "WAITING"):
            #     #error case
            #     pass    
            # # OK message: i want to see it
            # data2 = clientSock.recv(64)
            # print(data2.decode("UTF-8").strip())
        
        # works up till here

        # integer sequence number> <space> <integer ACK number> <space> 
        # <20 bytes of characters – payload> <space> 
        # <integer checksum represented as characters>
        
        chunk_size = 20
        seq_bool = False        # expects this to be the same
        ack_bool = False        # expected to return the inverse of this
        
        # from: https://stackoverflow.com/a/61394102
        with open('declaration.txt') as fh:
            while (payload := fh.read(chunk_size)):

                # build the data packet
                
                # TESTING: breaking a packet on purpose: WORKS
                # seq_bool = not seq_bool if random.randint(0,10) > 7 else seq_bool

                chk_in = f"{1 if seq_bool else 0} {1 if ack_bool else 0} {payload}"
                chk_out = checksum(chk_in)
                packet = f"{chk_in} {chk_out}"

                # send packet and start the timer
                clientSock.sendall(bytes(packet, "UTF-8"))

                # recieve packet from the server
                buf = clientSock.recv(30)
                packetString = buf.decode("UTF-8")
                print(f"SERVER says: {packetString}")
                match: re.match = re.match(p_regex, packetString)

                # ack 0 is 00720 and ack 1 is 00721
                # NOTE: implement timeouts after. rdt 2.2 for now

                ack_bool = True if match[2] == '1' else False

                # ack bool should be the same as the most recently sent sequence number
                # so if ack is NOT the most recently sent or is corrupt              
                if ack_bool:
                    clientSock.sendall(bytes(packet, "UTF-8"))
                    buf = clientSock.recv(30)
                    packetString = buf.decode("UTF-8")
                    print(f"RESENT --- Server SAYS: {packetString}")
                    match: re.match = re.match(p_regex, packetString)
                
                # reset the timer and invert seq (ack need not be handled here)
                seq_bool = not seq_bool



    ##### END YOUR IMPLEMENTATION HERE #####

    print("Finish running sender: {}".format(datetime.datetime.now()))

    # PRINT STATISTICS
    # PLEASE DON'T ADD ANY ADDITIONAL PRINT() AFTER THIS LINE
    print("File checksum: {}".format(checksum_val))
    print("Total packet sent: {}".format(total_packet_sent))
    print("Total packet recv: {}".format(total_packet_recv))
    print("Total corrupted packet recv: {}".format(total_corrupted_pkt_recv))
    print("Total timeout: {}".format(total_timeout))

    return (checksum_val, total_packet_sent, total_packet_recv, total_corrupted_pkt_recv, total_timeout)
 
if __name__ == '__main__':
    # CHECK INPUT ARGUMENTS
    # if len(sys.argv) != 9:
    #     print("Expected \"python3 PA2_sender.py <server_ip> <server_port> <connection_id> <loss_rate> <corrupt_rate> <max_delay> <transmission_timeout> <filename>\"")
    #     exit()

    # ASSIGN ARGUMENTS TO VARIABLES
    # server_ip, server_port, connection_ID, loss_rate, corrupt_rate, max_delay, transmission_timeout, filename = sys.argv[1:]

    # TEMPORARY RESOLUTION FOR LOCALHOST
    server_ip, server_port, connection_ID, loss_rate, corrupt_rate, max_delay, transmission_timeout, filename \
    =  "127.0.0.1", 1025, 6464, 0.0, 0.0, 0.0, 60, "declaration.txt"
    
    # RUN SENDER
    start_sender(server_ip, int(server_port), connection_ID, loss_rate, corrupt_rate, max_delay, float(transmission_timeout), filename)
