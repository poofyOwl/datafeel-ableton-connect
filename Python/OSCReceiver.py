from pythonosc import dispatcher, osc_server
import asyncio
import sys
from time import sleep
from datafeel.device import VibrationMode, discover_devices, LedMode, ThermalMode

from utils import *
from OSCMessageHandlerMIDI import OSCMessageHandlerMIDI

# Discover DataFeel devices
devices = discover_devices(4)
if not devices:
    print("No DataFeel devices found. Exiting...")
    sys.exit(1)

async def run_osc_server():
    # first run the MIDI one
    osc_msg_handler_midi = OSCMessageHandlerMIDI(devices)
    disp = dispatcher.Dispatcher()
    disp.map("/*", osc_msg_handler_midi.handle_osc_message)
    server = osc_server.AsyncIOOSCUDPServer(("0.0.0.0", OSC_PORT_MIDI), disp, asyncio.get_event_loop())
    transport, protocol = await server.create_serve_endpoint()
    print(f"Listening for OSC messages on port {OSC_PORT_MIDI}...")
    
    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        print("\nExiting...")
        sys.exit(0)

if __name__ == "__main__":
    asyncio.run(run_osc_server())
