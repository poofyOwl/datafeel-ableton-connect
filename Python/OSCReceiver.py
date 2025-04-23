from pythonosc import dispatcher, osc_server
import asyncio
import sys
from time import sleep
from datafeel.device import discover_devices

from utils import *
from OSCMessageHandlerMIDI import OSCMessageHandlerMIDI
from OSCMsgHandlerMIDIInstrument import OSCMessageHandlerMIDIInstrument, InstrDotMap
from OSCMessageHandlerFX import OSCMessageHandlerFX

# Discover DataFeel devices
devices = discover_devices(4)
if not devices:
    print("No DataFeel devices found...")
    sys.exit(1)

async def run_osc_server():
    # MIDI Instrument Handlers
    osc_msg_handler_kick = OSCMessageHandlerMIDIInstrument(devices, InstrDotMap.KICK)
    osc_msg_handler_snare = OSCMessageHandlerMIDIInstrument(devices, InstrDotMap.SNARE)
    osc_msg_handler_bass = OSCMessageHandlerMIDIInstrument(devices, InstrDotMap.BASS)

    # FX handler
    osc_msg_handler_fx = OSCMessageHandlerFX(devices)

    disp = dispatcher.Dispatcher()
    disp.map("/Velocity*", osc_msg_handler_kick.handle_osc_message)
    disp.map("/Note*", osc_msg_handler_kick.handle_osc_message)
    disp.map("/Velocity*", osc_msg_handler_snare.handle_osc_message)
    disp.map("/Note*", osc_msg_handler_snare.handle_osc_message)
    disp.map("/Velocity*", osc_msg_handler_bass.handle_osc_message)
    disp.map("/Note*", osc_msg_handler_bass.handle_osc_message)
    disp.map("/pan", osc_msg_handler_fx.handle_osc_message)
    disp.map("/volume", osc_msg_handler_fx.handle_osc_message)

    # server = osc_server.AsyncIOOSCUDPServer(("0.0.0.0", OSC_PORT_MIDI), disp, asyncio.get_event_loop())
    # transport, protocol = await server.create_serve_endpoint()
    # print(f"Listening for OSC messages on port {OSC_PORT_MIDI}...")

    server = osc_server.AsyncIOOSCUDPServer(("0.0.0.0", OSC_PORT_MIDI_KICK), disp, asyncio.get_event_loop())
    transport, protocol = await server.create_serve_endpoint()
    print(f"Listening for OSC messages on port {OSC_PORT_MIDI_KICK}...")
    server = osc_server.AsyncIOOSCUDPServer(("0.0.0.0", OSC_PORT_MIDI_SNARE), disp, asyncio.get_event_loop())
    transport, protocol = await server.create_serve_endpoint()
    print(f"Listening for OSC messages on port {OSC_PORT_MIDI_SNARE}...")
    server = osc_server.AsyncIOOSCUDPServer(("0.0.0.0", OSC_PORT_MIDI_BASS), disp, asyncio.get_event_loop())
    transport, protocol = await server.create_serve_endpoint()
    print(f"Listening for OSC messages on port {OSC_PORT_MIDI_BASS}...")
    server = osc_server.AsyncIOOSCUDPServer(("0.0.0.0", OSC_PORT_FX_VIBRATION), disp, asyncio.get_event_loop())
    transport, protocol = await server.create_serve_endpoint()
    print(f"Listening for OSC messages on port {OSC_PORT_FX_VIBRATION}...")
    
    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        print("\nExiting...")
        sys.exit(0)

if __name__ == "__main__":
    asyncio.run(run_osc_server())
