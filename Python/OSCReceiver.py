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
    # Old MIDI handler
    # server = osc_server.AsyncIOOSCUDPServer(("0.0.0.0", OSC_PORT_MIDI), disp, asyncio.get_event_loop())
    # transport, protocol = await server.create_serve_endpoint()
    # print(f"Listening for OSC messages on port {OSC_PORT_MIDI}...")

    # MIDI Kick Handler
    osc_msg_handler_kick = OSCMessageHandlerMIDIInstrument(devices, InstrDotMap.KICK)
    disp_kick = dispatcher.Dispatcher()
    disp_kick.map("/Note*", osc_msg_handler_kick.handle_osc_message)
    disp_kick.map("/Velocity*", osc_msg_handler_kick.handle_osc_message)
    server_kick = osc_server.AsyncIOOSCUDPServer(("0.0.0.0", OSC_PORT_MIDI_KICK), disp_kick, asyncio.get_event_loop())
    transport, protocol = await server_kick.create_serve_endpoint()
    print(f"Listening for OSC messages on port {OSC_PORT_MIDI_KICK}...")

    # MIDI Snare Handler
    osc_msg_handler_snare = OSCMessageHandlerMIDIInstrument(devices, InstrDotMap.SNARE)
    disp_snare = dispatcher.Dispatcher()
    disp_snare.map("/Note*", osc_msg_handler_snare.handle_osc_message)
    disp_snare.map("/Velocity*", osc_msg_handler_snare.handle_osc_message)
    server_snare = osc_server.AsyncIOOSCUDPServer(("0.0.0.0", OSC_PORT_MIDI_SNARE), disp_snare, asyncio.get_event_loop())
    transport, protocol = await server_snare.create_serve_endpoint()
    print(f"Listening for OSC messages on port {OSC_PORT_MIDI_SNARE}...")

    # MIDI Bass Handler
    osc_msg_handler_bass = OSCMessageHandlerMIDIInstrument(devices, InstrDotMap.BASS)
    disp_bass = dispatcher.Dispatcher()
    disp_bass.map("/Note*", osc_msg_handler_bass.handle_osc_message)
    disp_bass.map("/Velocity*", osc_msg_handler_bass.handle_osc_message)
    server_bass = osc_server.AsyncIOOSCUDPServer(("0.0.0.0", OSC_PORT_MIDI_BASS), disp_bass, asyncio.get_event_loop())
    transport, protocol = await server_bass.create_serve_endpoint()
    print(f"Listening for OSC messages on port {OSC_PORT_MIDI_BASS}...")

    # FX handler
    osc_msg_handler_fx = OSCMessageHandlerFX(devices)
    disp_fx = dispatcher.Dispatcher()
    disp_fx.map("/pan", osc_msg_handler_fx.handle_osc_message)
    disp_fx.map("/volume", osc_msg_handler_fx.handle_osc_message)
    server_fx = osc_server.AsyncIOOSCUDPServer(("0.0.0.0", OSC_PORT_FX_VIBRATION), disp_fx, asyncio.get_event_loop())
    transport, protocol = await server_fx.create_serve_endpoint()
    print(f"Listening for OSC messages on port {OSC_PORT_FX_VIBRATION}...")

    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        print("\nExiting...")
        sys.exit(0)

if __name__ == "__main__":
    asyncio.run(run_osc_server())
