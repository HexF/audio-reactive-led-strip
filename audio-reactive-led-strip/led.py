from __future__ import print_function
from __future__ import division

import platform
import numpy as np
import config
import socket


_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

_gamma = np.load(config.GAMMA_TABLE_PATH)
"""Gamma lookup table used for nonlinear brightness correction"""

_prev_pixels = np.tile(253, (3, config.N_PIXELS))
"""Pixel values that were most recently displayed on the LED strip"""

pixels = np.tile(1, (3, config.N_PIXELS))
"""Pixel values for the LED strip"""


def update():
    """Sends UDP packets to ESP8266 to update LED strip values

    The ESP8266 will receive and decode the packets to determine what values
    to display on the LED strip. The communication protocol supports LED strips
    with a maximum of 2^16 LEDs.

    The packet encoding scheme is:
        |h|l|r|g|b|
    where
        l (0 to 255): Low byte of LED Index
        h (0 to 255): High byte of LED Index
        r (0 to 255): Red value of LED
        g (0 to 255): Green value of LED
        b (0 to 255): Blue value of LED
    """
    global pixels, _prev_pixels
    # Truncate values and cast to integer
    pixels = np.clip(pixels, 0, 255).astype(int)
    # Optionally apply gamma correc tio
    p = _gamma[pixels] if config.SOFTWARE_GAMMA_CORRECTION else np.copy(pixels)
    MAX_PIXELS_PER_PACKET = 1024//5
    # Pixel indices
    idx = range(pixels.shape[1])
    idx = [i for i in idx if not np.array_equal(p[:, i], _prev_pixels[:, i])]
    n_packets = len(idx) // MAX_PIXELS_PER_PACKET + 1
    idx = np.array_split(idx, n_packets)
    for packet_indices in idx:
        m = []
        for i in packet_indices:
            m.append(i>>8)
            m.append(i & 0xFF)  # Index of pixel to change
            
            m.append(p[0][i])  # Pixel red value
            m.append(p[1][i])  # Pixel green value
            m.append(p[2][i])  # Pixel blue value
        m = bytes(m)

        _sock.sendto(m, (config.UDP_IP, config.UDP_PORT))
    _prev_pixels = np.copy(p)
