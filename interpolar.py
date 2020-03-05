from itertools import chain, zip_longest

string1 = 'aovces'
string2 = 'm o'

interpolation = zip_longest(string1, string2, fillvalue='')
print(''.join(chain(*interpolation)))