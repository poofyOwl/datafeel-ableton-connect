from time import time

from utils import *
from OSCMessageHandlerBase import *
from random import randint


class OSCMessageHandlerMIDI(OSCMessageHandlerBase):
    '''
    MIDI messages will always be sent in pairs, first one for Velocity and then one for Note.
    
    When receiving Velocity message, set the dot vibration intensity.
    If intensity is 0, stop dot vibration.
    
    Then when receiving the Note message, if intensity is 0, ignore the Note. 
    If intensity is not 0, set the dot frequency and start vibration.
    '''

    def __init__(self, devices):
        super().__init__(devices)
        # TODO TEMP
        # devices[0].registers.set_vibration_mode(VibrationMode.MANUAL)
        # self.devices[0].registers.set_vibration_intensity(0.5)

        self._intensity = -1
        self._note = -1

        # for handling many consecutive messages eg multiple notes being played at the same time
        self._message_burst_happening = False
        self._prev_message_time = 0
        self._message_burst_start_time = 0
        self._message_burst_queue = []

    def handle_osc_message(self, address, *args):
        message_time = time()
        print(f"{message_time} Received OSC Message: {address} {args}")
        
        if self._message_burst_happening:
            if message_time - self._message_burst_start_time > MESSAGE_BURST_MAX_TIME_S:
                # burst done, process the burst of messages and reset
                print("burst done")
                self._handle_command_burst()
                self._message_burst_queue.clear()
                self._message_burst_happening = False
                # then handle the message as normal
            else: # still receiving burst
                print("keep receiving burst")
                self._message_burst_queue.append((address, args))

        else:
            if str(address[1:9]) == "Velocity" and message_time - self._prev_message_time < MESSAGE_BURST_MAX_TIME_S:
                # start message burst
                print("start burst")
                self._message_burst_happening = True
                self._message_burst_queue.append((address, args))
                self._message_burst_start_time = message_time
            else: # handle single command
                self._handle_single_command(address, args)
                self._prev_message_time = message_time

    def _handle_single_command(self, address, args):
        # print("single command")
        command = str(address[1:])
        # index = int(address[-1])
        # print(command)
        # print(index)

        if command[:8] == "Velocity": 
            try:
                velocity = args[0]
                self._intensity = velocity/127

                # if self._intensity == 0:
                #     # TODO for now just using 1 dot
                #     print("stopping vibration")
                #     # self.devices[0].stop_vibration()
                # else:
                #     print(f"Setting intensity to {self._intensity}")
                #     self.devices[0].registers.set_vibration_intensity(self._intensity)
            except ValueError:
                print("Invalid vibration parameters.")

        elif command[:4] == "Note": 
            try:
                self._note = args[0]
                if self._intensity != 0:
                    # frequency = noteToFreq(self._note)
                    color = int(self._note * 255 / 127)
                    # print(f"setting frequency {frequency}")
                    print(f"setting color {color}")
                    # self.devices[0].registers.set_vibration_frequency(frequency)
                    self.devices[0].set_led(randint(0,255),randint(0,255),randint(0,255))
                    # self.devices[0].set_led(0,color,0)
            except ValueError:
                print("Invalid light parameters.")

        else:
            print("Unknown command or incorrect parameters.")

    def _handle_command_burst(self):
        pass