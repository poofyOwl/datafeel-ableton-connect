from time import time
from datafeel.device import discover_devices

devices = discover_devices(4)
device = devices[0]
print(device)  

print(f"{time()} led")
device.set_led(255, 0, 0)
print(f"{time()} led return")