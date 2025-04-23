from typing import List
from datafeel.device import Dot

class OSCMessageHandlerBase:

    def __init__(self, devices: List[Dot]):
        self.devices = devices

    def handle_osc_message(self, address, *args):
        print(f"Received OSC Message: {address} {args}")
