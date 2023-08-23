#!/usr/bin/env python

import time
from globus_compute_sdk import Client
gcc = Client()

functionID='6cde8b5a-6517-4703-bed0-456bfc78fbe1'
endpointID='0390d320-3c26-4459-840a-8a0116d95cc8'

# Call the remote function and return its UUID
taskID = gcc.run(endpoint_id=endpointID, function_id=functionID)

# Wait for the function to complete
while True:
    try:
        print(f"Result from {taskID}: {gcc.get_result(taskID)}")
        break
    except Exception as e:
        print("Waiting for result...")
        time.sleep(1)

