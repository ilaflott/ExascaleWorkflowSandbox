#!/usr/bin/env python

from globus_compute_sdk import Client

gcc = Client()
def hello_world():
    import socket
    return (f"hello from {socket.gethostname()}")

func_uuid = gcc.register_function(hello_world)
print(func_uuid)
