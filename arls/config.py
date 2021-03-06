"""Settings for audio reactive LED strip"""
from __future__ import print_function
from __future__ import division
import os
import configparser

cfg = configparser.ConfigParser()
cfg.read_dict({
    'general': {
        'fps': '60',
        'visualization': 'energy'
    },
    'controller': {
        'ip':'127.0.0.1',
        'port': '7777',
        'pixel_count': '50'
    },
    'microphone': {
        'sample_frequency': '44100'
    },
    'dsp': {
        'min_frequency': '200',
        'max_frequency': '12000',
        'fft_bins': '24',
        'min_volume_threshold': '1e-7',
        'history_frames': '2'
    }
})

cfg.read('/etc/arls.cfg') # Import from /etc/ first
cfg.read(os.path.expanduser('~/.config/audio-reactive-led-strip/config')) # Then allow user overrides

UDP_IP = cfg['controller']['ip']
"""IP address of the ESP8266. Must match IP in esp32.ino"""
UDP_PORT = int(cfg['controller']['port'])
"""Port number used for socket communication between Python and ESP8266"""
SOFTWARE_GAMMA_CORRECTION = False
"""Set to False because the firmware handles gamma correction + dither"""

N_PIXELS = int(cfg['controller']['pixel_count'])
"""Number of pixels in the LED strip (must match ESP8266 firmware)"""

GAMMA_TABLE_PATH = os.path.join(os.path.dirname(__file__), 'gamma_table.npy')
"""Location of the gamma correction table"""

MIC_RATE = int(cfg['microphone'].get('sample_frequency',fallback="44100"))
"""Sampling frequency of the microphone in Hz"""

_max_led_FPS = int(((N_PIXELS * 30e-6) + 50e-6)**-1.0)
FPS = int(cfg['general'].get('fps', fallback=str(_max_led_FPS)))
"""Desired refresh rate of the visualization (frames per second)

FPS indicates the desired refresh rate, or frames-per-second, of the audio
visualization. The actual refresh rate may be lower if the computer cannot keep
up with desired FPS value.

Higher framerates improve "responsiveness" and reduce the latency of the
visualization but are more computationally expensive.

Low framerates are less computationally expensive, but the visualization may
appear "sluggish" or out of sync with the audio being played if it is too low.

The FPS should not exceed the maximum refresh rate of the LED strip, which
depends on how long the LED strip is.
"""
assert FPS <= _max_led_FPS, 'FPS must be <= {}'.format(_max_led_FPS)

MIN_FREQUENCY = int(cfg['dsp'].get('min_frequency', fallback="2"))
"""Frequencies below this value will be removed during audio processing"""

MAX_FREQUENCY = int(cfg['dsp'].get('max_frequency', fallback="2"))
"""Frequencies above this value will be removed during audio processing"""

N_FFT_BINS = int(cfg['dsp'].get('fft_bins', fallback="2"))
"""Number of frequency bins to use when transforming audio to frequency domain

Fast Fourier transforms are used to transform time-domain audio data to the
frequency domain. The frequencies present in the audio signal are assigned
to their respective frequency bins. This value indicates the number of
frequency bins to use.

A small number of bins reduces the frequency resolution of the visualization
but improves amplitude resolution. The opposite is true when using a large
number of bins. More bins is not always better!

There is no point using more bins than there are pixels on the LED strip.
"""

N_ROLLING_HISTORY = int(cfg['dsp'].get('history_frames',fallback="2"))
"""Number of past audio frames to include in the rolling window"""

MIN_VOLUME_THRESHOLD = float(cfg['dsp'].get('min_volume_threshold',fallback="1e-7"))
"""No music visualization displayed if recorded audio volume below threshold"""

VISUALIZATION = cfg['general'].get('visualization', fallback='energy')
"""Name of function from within visualizations.py"""