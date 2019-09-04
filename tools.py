import pydub
import numpy as np


sample_rate = 16000
amp_thresh = 15000


def open_mp3(path):
    f = pydub.AudioSegment.from_mp3(path)
    return np.array(f.get_array_of_samples()).reshape(-1)


def waves_from_array(arr):
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
    arr = []
    for amp, l in w:
        wav = np.arange(l) / l
        wav = amp * np.sin(2 * np.pi * wav)
        arr.extend(wav)
    return np.array(arr)


def waves_in_range(w, r):
    rsum = np.cumsum([l for _, l in w])
    ii = np.where((rsum < r[1]) & (rsum > r[0]))[0]
    return [w[i] for i in ii]


def true_pentatonic_freqs(octave=2, position=1, descending=False):
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
    d = 2**(1/12)
    t = (tf + tf*d)/2
    b = (tf + tf/d)/2
    return b, t