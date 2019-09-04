import sys
import numpy as np
from tools import *


def main(filename, step):
    z = open_mp3(filename)
    nfs = []
    for t in range(0, z.size, step):
        x = z[t:min(t + step, z.size)]
        if max(x) > amp_thresh:  # filter out end
            wvs = np.fft.fft(x)[:len(x) // 2]
            nfs.append(sample_rate * np.argsort(wvs) / step)
    best_fit = (None, -1)
    for octave in range(0, 9):
        for position in range(1, 6):
            for descending in [False, True]:
                tfs = true_pentatonic_freqs(
                    octave=octave,
                    position=position,
                    descending=descending)
                score = 0
                for n in nfs:
                    true_note = next(tfs)
                    r = note_range(true_note)
                    hits = np.where((r[0] < n) & (n < r[1]))[0]
                    if hits.size > 0:
                        score += max(hits)
                if score > best_fit[1]:
                    best_fit = ((octave, position, descending), score)

    result = 'You played a{} A-minor pentatonic scale in the {}{} position!'.format(
        ' descending' if best_fit[0][2] else 'n ascending',
        best_fit[0][1],
        'st' if best_fit[0][1] == 1 else
        'nd' if best_fit[0][1] == 2 else
        'rd' if best_fit[0][1] == 3 else
        'th'
    )
    print(result)


if __name__ == '__main__':
    f = sys.argv[1]
    s = 12000 if f == 'data/AmPent_1st.mp3' else 8000
    main(f, s)
