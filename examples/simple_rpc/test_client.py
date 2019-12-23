from __future__ import print_function
from __future__ import absolute_import
from time import sleep
import os
import random
from vnpy.rpc import RpcClient


class TestClient(RpcClient):
    """
    Test RpcClient
    """
    client_name = ""
    def __init__(self):
        """
        Constructor
        """
        super(TestClient, self).__init__()
        self.client_name=os.getpid()

    def callback(self, topic, data):
        """
        Realize callable function
        """
        print(f"client {self.client_name} received topic:{topic}, data:{data}")


if __name__ == "__main__":
    req_address = "tcp://localhost:2014"
    sub_address = "tcp://localhost:4102"

    tc = TestClient()
    tc.subscribe_topic("ping")
    tc.start(req_address, sub_address)

    while 1:
        print(tc.add(random.randint(1,100), random.randint(1,200)))
        sleep(2)
        print(tc.sub(random.randint(1,100), random.randint(1,200)))
        sleep(2)
