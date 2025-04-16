class OSCMessageHandlerBase:

    def __init__(self, devices):
        self.devices = devices

    def handle_osc_message(self, address, *args):
        print(f"Received OSC Message: {address} {args}")
