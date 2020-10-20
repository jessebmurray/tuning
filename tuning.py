import matplotlib.pyplot as plt
import numpy as np
import math as m
from IPython.display import Markdown, display


intervalsFull = ['Perfect Consonant, Perfect Octave', 'Perfect Consonant, Perfect Fifth', \
                 'Perfect Consonant, Perfect Fourth', 'Imperfect Consonant, Major Third', \
                 'Imperfect Consonant, Minor Third', 'Disonnant, Major Second', \
                 'Dissonant, Minor Second']
inverse_intervalsFull = ['Perfect Consonant, Perfect Unison', 'Perfect Consonant, Perfect Fourth', \
                         'Perfect Consonant, Perfect Fifth', 'Imperfect Consonant, Minor Sixth', \
                         'Imperfect Consonant, Major Sixth', 'Dissonant, Minor Seventh', \
                         'Dissonant, Major Seventh']
semitones = [12, 7, 5, 4, 3, 2, 1]
inverse_semitones = [12 - value for value in semitones]

pythagorean_numerators = [2, 3, 4, 81, 32, 9, 256]
pythagorean_denominators = [1, 2, 3, 64, 27, 8, 243]
inverse_pythagorean_numerators = [1, 4, 3, 128, 27, 16, 243]
inverse_pythagorean_denominators = [1, 3, 2, 81, 16, 9, 128]



plt.style.use('seaborn')
plt.style.use('seaborn-talk')
import seaborn as sns

intervals = [row.split(', ')[1] for row in intervalsFull]
intervals_type = [row.split(', ')[0] for row in intervalsFull]
inverse_intervals = [row.split(', ')[1] for row in inverse_intervalsFull]
inverse_intervals_type = [row.split(', ')[0] for row in inverse_intervalsFull]


def printmd(string):
    display(Markdown(string))


def plot_waves(top, bottom, inverse=False, num_show=2):
    errors = list()
    perrors = list()
    inverse_errors = list()
    pinverse_errors = list()

    if inverse is False:
        halfsteps = semitones[top - 2]
        printmd(intervals[top - 2])
        print('(', intervals_type[top - 2], ')', sep='')
    else:
        halfsteps = inverse_semitones[bottom - 2]
        printmd(inverse_intervals[bottom - 2])
        print('(', inverse_intervals_type[bottom - 2], ')', sep='')
        print('Inverse of', intervals[bottom - 2])

    twelvetone = 2 ** (halfsteps / 12)

    if inverse:
        ptop = inverse_pythagorean_numerators[bottom - 2]
        pbottom = inverse_pythagorean_denominators[bottom - 2]
    else:
        ptop = pythagorean_numerators[top - 2]
        pbottom = pythagorean_denominators[top - 2]
    print(halfsteps, 'semitones')
    print()

    # Twelve-tone description
    print('Twelve-Tone Equal Temperament:')
    print('2 ^ (', halfsteps, ' / 12)', sep='')
    print('As Decimal:')
    print(round(twelvetone, 4))
    print()

    # Proposed tuning description
    print('Proposed tuning:')
    if top % 2 == 0 and bottom % 2 == 0:
        top = int(top / 2)
        bottom = int(bottom / 2)
        print(top * 2, '/', bottom * 2, '=', top, '/', bottom)
    else:
        print(top, '/', bottom)
    frac = top / bottom
    print('As Decimal:')
    print(frac)
    print()

    # Pythagorean tuning description
    print('Pythagorean tuning:')

    print(ptop, '/', pbottom)
    pfrac = ptop / pbottom
    print('As Decimal:')
    print(pfrac)
    print()

    # Proposed error
    error = (twelvetone - frac) / twelvetone
    print('Error between Proposed tuning and Twelve-tone equal temperament:\n', \
          "{0:.3f}%".format(100 * error), sep='')
    if inverse:
        inverse_errors.append(error)
    else:
        errors.append(error)

    # Pythagorean error
    perror = (twelvetone - pfrac) / twelvetone
    print('Error between Pythagorean tuning and Twelve-tone equal temperament:\n', \
          "{0:.3f}%".format(100 * perror), sep='')
    if inverse:
        pinverse_errors.append(perror)
    else:
        perrors.append(perror)

    periods = bottom * num_show
    x = np.arange(0, periods, 0.01)
    y1 = np.cos(2 * m.pi * x)

    ey2 = np.cos(2 * m.pi * twelvetone * x)
    ey2sum = y1 + ey2
    plt.subplot(4, 1, 1)
    plt.title('Twelve-tone equal temperament: ' + str(twelvetone))
    plt.plot(x, y1)
    plt.plot(x, ey2)
    plt.show()

    y2 = np.cos(2 * m.pi * frac * x)
    y2sum = y1 + y2
    plt.subplot(4, 1, 2)
    plt.title('Proposed: ' + str(top) + '/' + str(bottom))
    plt.plot(x, y1)
    plt.plot(x, y2)
    plt.show()

    py2 = np.cos(2 * m.pi * pfrac * x)
    py2sum = y1 + py2
    plt.subplot(4, 1, 3)
    plt.title('Pythagorean: ' + str(ptop) + '/' + str(pbottom))
    plt.plot(x, y1)
    plt.plot(x, py2)
    plt.show()

    plt.subplot(4, 1, 4)
    plt.title('Twelve-tone equal temperament: ' + str(round(twelvetone, 6)) + \
              ' summed. (How the interval sounds)')
    plt.plot(x, ey2sum)
    plt.show()

    plt.subplot(4, 1, 1)
    plt.title('Proposed: ' + str(top) + '/' + str(bottom) + ' summed. (How the interval sounds)')
    plt.plot(x, y2sum)
    plt.show()

    plt.subplot(4, 1, 2)
    plt.title('Pythagorean: ' + str(ptop) + '/' + str(pbottom) + ' summed. (How the interval sounds)')
    plt.plot(x, py2sum)
    plt.show()

    plt.subplot(4, 1, 3)
    plt.title('Twelve-tone minus Proposed. (How out of tune the interval sounds)')
    twelve_proposed = ey2sum - y2sum
    plt.plot(x, twelve_proposed)
    plt.show()

    plt.subplot(4, 1, 4)
    plt.title('Twelve-tone minus Pythagorean. (How out of tune the interval sounds)')
    twelve_pythagorean = ey2sum - py2sum
    plt.plot(x, twelve_pythagorean)
    plt.show()

    if top != 7 or bottom != 4:
        for i in range(5):
            print()

        print('Proposed Tuning Algorithm:')
        if inverse:
            print('Add 1 to the numerator and denominator of the ', \
                  'last non-inverse fraction: ', str(bottom) + ' / ' + str(int((top / 2))), \
                  sep='')
        else:
            print('Multiply the denominator by 2 and switch the numerator and denominator',
                  ' to get the inverse.', sep='')

    for i in range(98):
        print('_', end='')
    print('\n')


def show_algorithm():
    for numerator in range(2, 9):
        denominator = numerator - 1
        plot_waves(numerator, denominator, num_show=5)
        plot_waves(2 * denominator, numerator, inverse=True, num_show=5)


def get_tuning():
    errors = list()
    perrors = list()
    inverse_errors = list()
    pinverse_errors = list()
    for numerator in range(2, 9):
        denominator = numerator - 1
        errors, perrors, inverse_errors, pinverse_errors = get_waves(
            errors, perrors, inverse_errors, pinverse_errors, numerator, denominator, num_show=5)
        errors, perrors, inverse_errors, pinverse_errors = get_waves(
            errors, perrors, inverse_errors, pinverse_errors, 2 * denominator, numerator, inverse=True, num_show=5)

    return errors, perrors, inverse_errors, pinverse_errors


def get_waves(errors, perrors, inverse_errors, pinverse_errors, top, bottom, inverse=False, num_show=2):
    if inverse is False:
        halfsteps = semitones[top - 2]

    else:
        halfsteps = inverse_semitones[bottom - 2]

    twelvetone = 2 ** (halfsteps / 12)

    if inverse:
        ptop = inverse_pythagorean_numerators[bottom - 2]
        pbottom = inverse_pythagorean_denominators[bottom - 2]
    else:
        ptop = pythagorean_numerators[top - 2]
        pbottom = pythagorean_denominators[top - 2]

    # Proposed tuning
    if top % 2 == 0 and bottom % 2 == 0:
        top = int(top / 2)
        bottom = int(bottom / 2)

    frac = top / bottom
    pfrac = ptop / pbottom

    # Proposed error
    error = (twelvetone - frac) / twelvetone
    if inverse:
        inverse_errors.append(error)
    else:
        errors.append(error)

    # Pythagorean error
    perror = (twelvetone - pfrac) / twelvetone
    if inverse:
        pinverse_errors.append(perror)
    else:
        perrors.append(perror)

    return errors, perrors, inverse_errors, pinverse_errors



errors, perrors, inverse_errors, pinverse_errors = get_tuning()


alltones = semitones + inverse_semitones
allerrors = errors + inverse_errors
pallerrors = perrors + pinverse_errors


def plot_errors():
    # plt.figure(figsize=(8,5.33333))
    plt.xticks(range(0, 13))
    plt.scatter(alltones, allerrors, label='Proposed errors with Twelve-tone', marker='s')
    plt.scatter(alltones, pallerrors, label='Pythagorean errors with Twelve-tone', marker='o')
    plt.axhline(y=0, linestyle='--')
    plt.title('Errors between Proposed, Pythagorean \n and Twelve-tone equal temperament')
    plt.xlabel('Semitones')
    plt.ylabel('Error')
    plt.legend()


def plot_abs_errors():
    # plt.figure(figsize=(8,5.33333))
    plt.xticks(range(0,13))
    plt.scatter(alltones, [abs(v) for v in allerrors], label='Proposed errors with Twelve-tone', marker='s')
    plt.scatter(alltones, [abs(v) for v in pallerrors], label='Pythagorean errors with Twelve-tone')
    plt.title('Absolute value of errors between Proposed, Pythagorean \n and Twelve-tone equal temperament')
    plt.xlabel('Semitones')
    plt.ylabel('Absolute Value of Error')
    plt.axhline(y=0, linestyle='--')
    plt.legend()