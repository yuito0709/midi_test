import rtmidi

midiout = rtmidi.MidiOut()
ports = midiout.get_ports()
print("利用可能なMIDIポート:")
for i, port in enumerate(ports):
    print(f"{i}: {port}")
midiout.close_port()
