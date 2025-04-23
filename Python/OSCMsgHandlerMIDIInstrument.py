from enum import Enum
from random import randint

from datafeel.device import LedMode

from utils import *
from OSCMessageHandlerBase import *

class InstrDotMap(Enum):
    # TODO future: there's probably a better way to model the dots and LEDs)
    # for now it's ([list of dots], [list of leds for each dot])
    KICK = ([1,2], [0,2,4,6])
    BASS = ([1,2], [1,3,5,7])
    SNARE = ([1,2], [8,9,10,11,12,13,14,15])

class OSCMessageHandlerMIDIInstrument(OSCMessageHandlerBase):
    '''
    MIDI messages will always be sent in pairs, first one for Velocity and then one for Note.
    
    When receiving Velocity message, set the light intensity for all the leds on all the dots 
    mapped to this class.
    If intensity is 0, turn off the lights.
    
    Then when receiving the Note message, if intensity is 0, ignore the Note. 
    If intensity is not 0, convert note to color and set the LEDs.
    '''

    def __init__(self, devices: List[Dot], instrument: InstrDotMap):
        # only keep subset of devices for this instrument according to the map
        devices_subset = []
        for index in instrument.value[0]:
            devices_subset.append(devices[index])
            devices[index].registers.set_led_mode(LedMode.OFF)
        super().__init__(devices_subset)

        self._leds = instrument.value[1]

        self._intensity = -1
        self._note = -1

    def handle_osc_message(self, address, *args):
        print(f"Received OSC Message: {address} {args}")
        
        command = str(address[1:])

        if command[:8] == "Velocity": 
            try:
                velocity = args[0]
                self._intensity = velocity/127

                # TODO change light intensity

            except ValueError:
                print("Invalid vibration parameters.")

        elif command[:4] == "Note": 
            try:
                self._note = args[0]
                if self._intensity != 0:
                    # TODO convert MIDI note to RGB
                    self._set_lights(self._intensity, randint(0,255),randint(0,255),randint(0,255))
            except ValueError:
                print("Invalid light parameters.")

        else:
            print("Unknown command or incorrect parameters.")
    
    def _set_lights(self, intensity, r, g, b):
        for device in self.devices:
            for led in self._leds:
                device.set_led(r, g, b, led)
