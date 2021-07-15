#!/usr/bin/env python3

import audioop
import math
import struct
import wave


def dump_list(sample_list, intensity=None, filename='test.wav'):
    if intensity is None:
        intensity = max(sample_list)

    with wave.open(filename, 'wb') as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(44100)

        for sample in sample_list:
            sample_i = int((sample % intensity) / intensity * 0x7fff)
            if sample_i < 0 or 0x7fff < sample_i:
                print(f"Sample : {sample}")
                print(f"Sample (int): {sample_i}")
            f.writeframes(struct.pack('<h', sample_i))

def dump_bytes(samples, filename='test.wav'):
    with wave.open(filename, 'wb') as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(44100)

        f.writeframes(samples)

def chirp():
    samples = [int(0x100 * math.cos(math.pow(x, 1.2)/100)) for x in range(100000)]

    return struct.pack('<' + 'h' * len(samples), *samples)

def glitchy_shepard():
    samples = [sum(int(0x50 * math.cos(math.pow(x, 1.4) / (2 ** y))) for y in range(20))
               for x in range(1000000)]
    print(samples[:100])
    return struct.pack('<' + 'h' * len(samples), *samples)


def main():
#    dump_list(range(100000), intensity=1000)
    dump_list([100, 100, 100, 0, 0, 0] * 10000, intensity=2000, filename='test2.wav')
    dump_list([200, 100, 200, 0, 100, 0] * 10000, intensity=2000, filename='test3.wav')
    dump_bytes(bytes([0x0f, 0xff, 0x0f, 0xff, 0x0f, 0xff, 0x0f, 0xff, 0, 0, 0, 0, 0, 0, 0, 0] * 8000), filename='test4.wav')
    dump_bytes(chirp(), filename='test5.wav')
    dump_bytes(glitchy_shepard(), filename='test6.wav')

if __name__ == "__main__":
    main()
