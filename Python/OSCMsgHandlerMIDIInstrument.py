from enum import Enum
from random import randint

from datafeel.device import LedMode

from utils import *
from OSCMessageHandlerBase import *

class InstrDotMap(Enum):
    # TODO future: there's probably a better way to model the dots and LEDs)
    # for now it's ([list of dots], [list of leds for each dot])
    BASS = ([1,2], [0,1,2,3,4,5,6,7])
    KICK = ([1,2], [9,11,13,15])
    SNARE = ([1,2], [8,10,12,14])

class OSCMessageHandlerMIDIInstrument(OSCMessageHandlerBase):
    '''
    MIDI messages will always be sent in pairs, first one for Velocity and then one for Note.
    
    When receiving Velocity message, set the velocity value.
    
    Then when receiving the Note message, if velocity is 0, turn off the lights.
    If intensity is not 0, convert note to color and set the LEDs.
    '''

    def __init__(self, devices: List[Dot], instrument: InstrDotMap):
        self._instrument = instrument
        
        # only keep subset of devices for this instrument according to the map
        devices_subset = []
        for index in instrument.value[0]:
            devices_subset.append(devices[index])
            devices[index].registers.set_led_mode(LedMode.INDIVIDUAL_MANUAL)
        super().__init__(devices_subset)

        self._leds = instrument.value[1]
        self._turn_leds_off()
        
        self._note = -1
        self._velocity = -1

    def handle_osc_message(self, address, *args):
        print(f"Received OSC Message in {self._instrument.name}: {address} {args}")
        
        command = str(address[1:])

        if command[:8] == "Velocity": 
            try:
                self._velocity = args[0]

            except ValueError:
                print("Invalid vibration parameters.")

        elif command[:4] == "Note": 
            try:
                if self._velocity == 0:
                    self._turn_leds_off()
                else:
                    self._note = args[0]
                    # TODO convert MIDI note to RGB
                    self._set_lights(randint(0,255),randint(0,255),randint(0,255))
            except ValueError:
                print("Invalid light parameters.")

        else:
            print("Unknown command or incorrect parameters.")
    
    def _set_lights(self, r, g, b):
        for device in self.devices:
            for led in self._leds:
                device.set_led(r, g, b, led)

    def _turn_leds_off(self):
        for device in self.devices:
            for led in self._leds:
                device.set_led(0, 0, 0, led)
