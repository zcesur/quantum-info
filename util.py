from string import ascii_uppercase

letter_dict = dict(zip(ascii_uppercase, xrange(26)))

def most_freq_ngrams(string, n, k):
    from collections import Counter
    ngrams = [string[i:i+n] for i in xrange(len(string)-n+1)]
    return Counter(ngrams).most_common(k)

def shift_letters(string, from_letter, to_letter):
    from re import search
    assert bool(search("^[A-Z]+$", string))
    
    shift = letter_dict[to_letter] - letter_dict[from_letter]
    return ''.join(
            ascii_uppercase[(letter_dict[letter]+shift)%26]
            for letter in string)

def substract_letters(minuend, substrahend):
    return ''.join(
            ascii_uppercase[((letter_dict[m]-letter_dict[s])%26)]
            for m, s in zip(minuend, substrahend))

def decypher(string, key, key_idx, period):
    d = dict(zip(key_idx, key))

    return ''.join(
            substract_letters(letter, d[idx%period])
            if idx%period in key_idx else '?'
            for idx, letter in enumerate(string))
