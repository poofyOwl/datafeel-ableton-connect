from pythonosc import dispatcher, osc_server
import asyncio
import sys
from time import sleep
from datafeel.device import VibrationMode, discover_devices, LedMode, ThermalMode

from utils import *
from OSCMessageHandlerBase import OSCMessageHandlerBase


class OSCMessageHandlerFX(OSCMessageHandlerBase):

    def handle_osc_message(address, *args):
        pass
