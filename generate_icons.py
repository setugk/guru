#!/usr/bin/env python3
"""Generate PWA icons for Guru app."""
import struct, zlib, math

def make_png(size):
    def chunk(name, data):
        c = zlib.crc32(name + data) & 0xffffffff
        return struct.pack('>I', len(data)) + name + data + struct.pack('>I', c)

    width = height = size
    ihdr = struct.pack('>IIBBBBB', width, height, 8, 2, 0, 0, 0)

    rows = []
    cx, cy, r = width/2, height/2, width*0.35
    sr = width * 0.12
    for y in range(height):
        row = b'\x00'
        for x in range(width):
            dx, dy = x - cx, y - cy
            dist = math.sqrt(dx*dx + dy*dy)
            in_circle = dist <= r
            in_drum = dist <= sr * 1.1
            if in_drum:
                row += bytes([60, 40, 30])
            elif in_circle:
                row += bytes([30, 20, 15])
            else:
                row += bytes([255, 255, 255])
        rows.append(row)

    raw = b''.join(rows)
    compressed = zlib.compress(raw)
    png = b'\x89PNG\r\n\x1a\n'
    png += chunk(b'IHDR', ihdr)
    png += chunk(b'IDAT', compressed)
    png += chunk(b'IEND', b'')
    return png

for size in [192, 512]:
    with open(f'icon-{size}.png', 'wb') as f:
        f.write(make_png(size))
    print(f'Generated icon-{size}.png')
