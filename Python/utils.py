OSC_PORT = 2390
OSC_PORT_MIDI = 2391

MESSAGE_BURST_MAX_TIME_S = 0.00001

def noteToFreq(note):
    a = 440 # frequency of A (common value is 440 Hz)
    return (a / 32) * (2 ** ((note - 9) / 12))

