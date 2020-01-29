from socket import *
from datetime import datetime
import time

# will want to change to host IP for mininet use
# specify host name and port for easier readability
serverName = 'Localhost'
serverPort = 12000

# create socket and set timeout
clientSocket = socket(AF_INET, SOCK_DGRAM)
clientSocket.settimeout(1)

# variables to tracking and calculating stats
numPings = 10
sequence = 1
minRtt = 0
maxRtt = 0
avgRtt = 0
packetsDropped = 0.0

while sequence <= numPings:
    # snapshot of time
    timeSent = datetime.now()

    # message to send, will need to append sequence and time to it
    message = 'This is Ping {}_{}'.format(sequence, timeSent)

    print message

    # send message to server and depending on reply do stuff
    clientSocket.sendto(message, (serverName, serverPort))

    try:
        returnMessage, serverAddress = clientSocket.recvfrom(1024)

        # return time
        timeReceived = datetime.now()
        print 'Return message from server received at {}'.format(timeReceived)
        print returnMessage

        # calculate RTT, td becomes timedelta object, rtt uses .total_seconds() to make more readable
        td = timeReceived - timeSent
        rtt = td.total_seconds()
        print 'RTT is {} seconds.\n'.format(rtt)

        # check min RTT
        if minRtt == 0:
            minRtt = rtt
        elif minRtt > rtt:
            minRtt = rtt

        # check max RTT
        if maxRtt == 0:
            maxRtt = rtt
        elif maxRtt < rtt:
            maxRtt = rtt

        # add to avg RTT so we can calculate later
        avgRtt = avgRtt + rtt

    except timeout:
        print 'Request timed out.  Packet {} lost.\n'.format(sequence)

        # add dropped packet
        packetsDropped += 1

    # increment sequence
    sequence += 1

clientSocket.close()

# RTT stats
print "RTT stats: "
print "rtt_min = {} rtt_max = {} rtt_avg = {}".format(minRtt, maxRtt, avgRtt/numPings)
print "Packet Loss: {}%".format(packetsDropped/numPings*100)