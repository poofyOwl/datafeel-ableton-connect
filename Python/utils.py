OSC_PORT = 2390
OSC_PORT_MIDI = 2391
OSC_PORT_VIBRATION = 2392
OSC_PORT_LIGHT = 2393
OSC_PORT_TEMPERATURE = 2394

MESSAGE_BURST_MAX_TIME_S = 0.00001

def noteToFreq(note):
    a = 440 # frequency of A (common value is 440 Hz)
    return (a / 32) * (2 ** ((note - 9) / 12))

def midi_to_rgb(midi_note):
    if not (0 <= midi_note <= 127):
        raise ValueError("MIDI note information recevied is not between 0 and 127")
    
    # Define bounds
    # C0
    min_note = 24
    # C8
    max_note = 120
    # Define RGB for Red & Sky Blue
    red = (255, 0, 0)
    yellow = (255, 255, 0)
    green = (0, 255, 0)
    cyan = (0, 255, 255)

    if midi_note <= min_note:
        return red
    elif midi_note >= min_note:
        return cyan
    else:
        # Normalize the note value to be 0.0 - 1.0
        midi_normalized = (midi_note - min_note) / (max_note - min_note)
        
        # Linearly interpolate each RGB channel
        r = int(red[0] + (cyan[0] - red[0]) * midi_normalized)
        g = int(red[1] + (cyan[1] - red[1]) * midi_normalized)
        b = int(red[2] + (cyan[2] - red[2]) * midi_normalized)

    return r, g, b