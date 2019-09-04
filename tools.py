import pydub
import numpy as np


sample_rate = 16000  # sampling rate for most mp3s
amp_thresh = 15000  # amplitude threshold to hear a note being played


def open_mp3(path):
    """
    Open an mp3 file and return as a numpy array
    :param path: mp3's relative filepath
    :return: a numpy array
    """
    f = pydub.AudioSegment.from_mp3(path)
    return np.array(f.get_array_of_samples()).reshape(-1)


def waves_from_array(arr):
    """
    Convert a numpy array to a series of sine waves that fits the original data best
    :param arr: a numpy array of audio data
    :return: an ordered list of sine waves represented as tuples of (amplitude, length in samples)
    """
    waves = []  # saved as (A, length of wave)
    prev = 0
    for t in range(1, arr.size):
        if arr[t-1] < 0 <= arr[t] or t == arr.shape[0] - 1:
            r = arr[prev:t]
            prev = t
            # save wave to list (in order)
            amp = max(abs(r))
            waves.append((amp, len(r)))
    return waves


def array_from_waves(w):
    """
    The inverse of waves_from_array
    :param w: an ordered list of sine waves represented as tuples of (amplitude, length in samples)
    :return: a numpy array
    """
    arr = []
    for amp, l in w:
        wav = np.arange(l) / l
        wav = amp * np.sin(2 * np.pi * wav)
        arr.extend(wav)
    return np.array(arr)


def waves_in_range(w, r):
    """
    Returns a sub-list of sine waves that occur within the range
    :param w: full list of sine waves
    :param r: a range represented as a tuple
    :return: a list of sine waves
    """
    rsum = np.cumsum([l for _, l in w])
    ii = np.where((rsum < r[1]) & (rsum > r[0]))[0]
    return [w[i] for i in ii]


def true_pentatonic_freqs(octave=2, position=1, descending=False):
    """
    A generator for A-minor pentatonic scale frequencies in order (based on parameters)
    :param octave: the octave of the first A note played in the scale (0 - 8 inclusive)
    :param position: the position of the scale (1 - 5 inclusive)
    :param descending: direction of the scale (boolean)
    :return: a generator of frequencies
    """
    ratios = [3, 2, 2, 3, 2]
    if descending:
        ratios = ratios[::-1]
    f = 27.5 * (2**octave)
    while position > 1:
        r = ratios.pop(0)
        ratios.append(r)
        f *= 2**(r/12)
        position -= 1
    while True:
        for r in ratios:
            yield f
            f *= 2**(r/12)


def note_range(tf):
    """
    Returns a range surrounding the true frequency of a note.  Any frequencies within the
    range can be considered the same note.
    :param tf: the true frequency of the note
    :return: a tuple representing a range
    """
    d = 2**(1/12)
    t = (tf + tf*d)/2
    b = (tf + tf/d)/2
    return b, t
