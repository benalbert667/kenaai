import sys
import numpy as np
import matplotlib.pyplot as plt
from tools import *


def main(filename, n=3):
    x = open_mp3(filename)
    x_waves = waves_from_array(x)
    look_for_note = []
    scores = []  # difference from ideal in number of samples, in order
    l_stack = []
    t = 0
    prev_t = 0
    for a, l in x_waves:
        look_for_note.append((a, prev_t + t))  # amplitude, start time of wave
        t += l
        l_stack.append(l)
        if t > sample_rate / n:  # 1/3 of a second + 2 win_exts
            # notes in recording are played at the start, so assume best position is at beginning of range
            score = max(look_for_note, key=lambda w: w[0])
            c = 1
            while score[1] - prev_t > sample_rate / (n * 2):  # seeing next note
                score = max(look_for_note[:-c], key=lambda w: w[0])
                c += 1
            score = (score[1] - prev_t, score[0])  # start of time wave relative to start of sec/n, amplitude
            look_for_note = look_for_note[-c:]
            if score[1] > 15000:  # filter out maxes from end
                scores.append((score, prev_t + score[0]))
            prev_t += sample_rate // n
            t = 0

    stats = np.array([s[0][0] for s in scores])
    ave_dev = np.average(np.abs(stats))
    accuracy = (1 - ave_dev / (sample_rate / (n * 2))) * 100  # 0% accuracy = 16000/(n*2)
    ii = range(1, len(stats) + 1)
    plt.bar(ii, stats / 16, color='black', label='deviation from beat (ms)')
    plt.xticks([], [])
    plt.title('%{:.2f} overall accuracy ({:.2f}ms average error)'.format(accuracy, ave_dev / 16))
    plt.legend()
    plt.show()


if __name__ == '__main__':
    main(sys.argv[1])
