#!/usr/bin/python3

#
# client.py
# Created by Stephen Brimhall on 2/21/17
# Copyright (c) Stephen Brimhall 2017. All Rights Reserved.
#

# Begin system imports
import socket
import json
# End system imports

class Client:
    """User-friendly networking client"""

    def __init__(self):
        """Takes an address and port of a server to connect to.
        Returns a new Client."""

        # Create socket
        self.sock = socket.socket()

        # Open connection
        self.sock.connect((address, port))

    def connect_to(self, address: str, port: str):
        """Connects the client to the given server"""

        server = (address, port)

        self.sock.connect(server)

    def transmit(self, message):
        """Takes data and transmits it as JSON."""

        json_str = json.dumps(message)

        self.__send(json_str)

        
    def __send(self message: str):
        """Takes a string, breaks it into parts, and sends it."""

        # Check the length of the message, if it is small enough, we'll send it.
        if len(message) < 3072:
            # Add 'last message' tag
            transmission = {"last": True, "data": message}

            # Convert new dict to json
            json_code = json.dumps(transmission)

            # Send json code, using utf-8 encoding
            self.sock.send(json_code.encode("utf-8"))

            # Return up the stream
            return

        # Ok, so we're at this point, it's not small enough. Time to split it.

        # Construct transmission, setting last to false
        transmission = {"last": False, "data": message[:3000]}

        # Convert new dict to json
        json_code = json.dumps(transmission)

        # Send json code, using utf-8 encoding
        self.sock.send(json_code.encode("utf-8"))

        # Recursively call the send function which will send the rest of the message
        self.__send(message[3000:])

    def receive(self):
        """Receive data by parts and decode it, returning the final result."""

        # Final result string, will be decoded at the end
        result = ""
        
        # Use a while loop, will break when receive final message
        while True:

            # recv call
            mesg = self.sock.recv().decode("utf-8")

            # Decode json from mesg
            mesg = json.loads(mesg)

            # Add data to result
            result += mesg['data']

            # Check if this is the last piece, if so, break the loop
            if mesg['last']:
                break

        # Whole message has been received. Decode JSON and return.
        result = json.loads(result)

        return result

    def close(self):
        """Close client connection"""
        
        self.sock.close()

    @classmethod
    def 
