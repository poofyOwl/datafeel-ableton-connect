from pythonosc import dispatcher, osc_server
import asyncio
import sys
from time import sleep
from datafeel.device import VibrationMode, discover_devices, LedMode, ThermalMode

from utils import *
from OSCMessageHandlerBase import OSCMessageHandlerBase


class OSCMessageHandlerFX(OSCMessageHandlerBase):

    def __init__(self, devices):
        super().__init__(devices)

        # TODO need to figure out how to get the track's volume if it is not sent to us over OSC
        self._intensity_volume_multiplier = 0.85 # for now init to 0.85 (0.0 dB in Ableton)

    def handle_osc_message(self, address, *args):
        print(f"Received OSC Message: {args}")

        if args[0] == '/pan':
            self._handle_pan(args[1])
        
        elif args[0] == '/volume':
            self._handle_volume(args[1])

    def _handle_pan(self, pan_value):
        '''
        Ableton OSC Pan goes from 0.0 (50L) to 1.0 (50R)
        When pan is center (0.5), all dots vibrate at 0.5 intensity
        When pan is all the way left (0.0), the 2 left dots vibrate at max intensity (1.0), and the 2 right dots are stopped (set intensity to 0.0). And vice versa for when pan is all the way right (1.0)
        Logic: 
            For the left dots: intensity = 1.0 - pan
            For the right dots: intensity = pan
        Left dots are devices 0 and 1, right dots are devices 2 and 3.
        Add volume multiplier!
        '''
        self.devices[0].registers.set_vibration_intensity((1.0 - pan_value)*self._intensity_volume_multiplier)
        self.devices[1].registers.set_vibration_intensity((1.0 - pan_value)*self._intensity_volume_multiplier)
        self.devices[2].registers.set_vibration_intensity(pan_value*self._intensity_volume_multiplier)
        self.devices[3].registers.set_vibration_intensity(pan_value*self._intensity_volume_multiplier)

    def _handle_volume(self, volume_value):
        '''
        Map volume fader to a vibration intensity multiplier. This multiplier will be applied to all the dots’ intensity that is based on the pan (above).
        Ableton OSC volume goes from 0.0 at -infinity to 1.0 at +6 dB. At 0.0 dB it’s 0.85
        Set the intensity multiplier of all the dots to the volume value received
        '''
        # set multiplier
        self._intensity_volume_multiplier = volume_value
        
        # first we need to get the current intensity of the dots
        intensities = []
        intensities.append(self.devices[0].registers.get_vibration_intensity())
        intensities.append(self.devices[1].registers.get_vibration_intensity())
        intensities.append(self.devices[2].registers.get_vibration_intensity())
        intensities.append(self.devices[3].registers.get_vibration_intensity())
        # now set 
        self.devices[0].registers.set_vibration_intensity(intensities[0]*self._intensity_volume_multiplier)
        self.devices[1].registers.set_vibration_intensity(intensities[1]*self._intensity_volume_multiplier)
        self.devices[2].registers.set_vibration_intensity(intensities[2]*self._intensity_volume_multiplier)
        self.devices[3].registers.set_vibration_intensity(intensities[3]*self._intensity_volume_multiplier)
