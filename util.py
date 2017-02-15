from string import ascii_uppercase

# Mapping from ASCII letters to integers modulo 26, i.e., the ring Z/26Z.
letter_dict = dict(zip(ascii_uppercase, xrange(26)))

def most_freq_ngrams(string, length, top=5):
    """Returns the most frequent n-grams that appear in a given string."""
    from collections import Counter
    ngrams = [string[i:i+length] for i in xrange(len(string)-length+1)]
    return Counter(ngrams).most_common(top)

def shift_letters(string, from_letter, to_letter):
    """Shifts the alphabet by some number of places such that from_letter
    becomes to_letter in a given string and returns the new string.
    """
    from re import search
    assert bool(search("^[A-Z]+$", string))
    
    shift = letter_dict[to_letter]-letter_dict[from_letter]
    return ''.join(
            ascii_uppercase[(letter_dict[letter]+shift) % 26]
            for letter in string)

def substract_letters(minuend, substrahend):
    """Performs modular substraction on the letters of the given strings
    based on their positions.
    """
    from re import search
    assert bool(search("^[A-Z]+$", minuend+substrahend))
    assert len(minuend) == len(substrahend)

    return ''.join(
            ascii_uppercase[((letter_dict[m]-letter_dict[s]) % 26)]
            for m, s in zip(minuend, substrahend))

def decipher(string, key):
    """Deciphers a string, which is encrypted with Vigenere cipher, using
    the given key and returns the new string. Both repeated and running keys
    can be used. In addition, partial keys can be supplied using '?' as a
    placeholder if some letters of the key is not known.
    """
    key_dict = {k:v for k,v in zip(xrange(len(key)), key) if v != '?'}

    return ''.join(
            substract_letters(letter, key_dict[idx % len(key)])
            if idx % len(key) in key_dict else '?'
            for idx, letter in enumerate(string))

def to_numeric_blocks(string, block_size):
    """Converts a string into a numeric matrix where block size determines
    the number of rows and each block of substrings corresponds to a
    column. Thus, in order to retrieve the string one needs to read the matrix
    in a column-major order.
    """
    import numpy as np
    from re import search
    
    assert bool(search("^[A-Z]+$", string))
    assert len(string) % block_size == 0
    
    numbers = [letter_dict[letter] for letter in string]
    return np.column_stack(tuple(
        numbers[i:i+block_size] for i in range(0, len(string), block_size)))
    
def to_string(numeric_blocks):
    import numpy as np

    # Flatten the matrix in column-major (Fortran-style) order
    array = np.asarray(numeric_blocks).ravel(order='F')
    return ''.join(ascii_uppercase[x] for x in array)

def hill_cipher(string, key):
    import numpy as np
        
    assert key.shape[0] == key.shape[1]

    plain_blocks = to_numeric_blocks(string, key.shape[0]) 
    encrypted_blocks = np.matmul(key, plain_blocks) % 26

    return to_string(encrypted_blocks)

def egcd(a, b):
    """Given two positive integers a, b, returns a triple (g, x, y) such
    that a*x + b*y = gcd(a,b).

    The algorithm and the implementation was found in the WikiBooks page
    'Extended Euclidean algorithm.'
    """
    if a == 0:
        return (b, 0, 1)
    else:
        g, x, y = egcd(b % a, a)
        return (g, y - (b // a) * x, x)

def mulinv(a, n):
    """Given a positive integer a and n, returns x, if it exists, such that
    ax = 1 mod n.

    The algorithm and the implementation was found in the WikiBooks page
    'Extended Euclidean algorithm.'
    """
    g, x, _ = egcd(a, n)
    if g == 1:
        return x % n
