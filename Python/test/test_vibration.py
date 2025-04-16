from time import time
from datafeel.device import VibrationMode, discover_devices

devices = discover_devices(4)
device = devices[0]
print(device)

device.registers.set_vibration_mode(VibrationMode.MANUAL)   

print(f"{time()} play")
device.play_frequency(110, 1.0)
print(f"{time()} play return")

print(f"{time()} stop command")
device.stop_vibration()
print(f"{time()} stop command return")
