import unittest


def solution(s):
    """
    Take in a string and returns the deciphered string.

    :param s: a cipher text string 
    :return: the deciphered string
    """
    if len(s) == 0:
        return ""

    max_supported_size = 1000000    # Arbitrarily limiting input string to 1MB for illustrative purposes

    if len(s) > max_supported_size:
        print("Try breaking the message into smaller chunks. Max supported message size =", max_supported_size, "bytes")
        return ""

    cipher_text = list(s)
    plain_text = ""

    a = ord('a')    # unicode code for 'a' is 97
    z = ord('z')    # unicode code for 'z' is 122
    alphabet_size = z-a+1     # assuming lowercase alphabet in range 97...122

    for character in cipher_text:

        if ord(character) in range(a, z+1):   # if the unicode equivalent of the character is in the specified range
            character = chr(a + (alphabet_size - (ord(character) - a))-1)    # decode the input character
        elif character not in range(a, z+1):
            character = character
        else:
            character = ' '
        plain_text = plain_text + character

    return str(plain_text)


class DecipherTests(unittest.TestCase):

    def test_1(self):
        cipher = "wrw blf hvv ozhg mrtsg'h vkrhlwv?"
        expected = "did you see last night's episode?"

        deciphered = solution(cipher)
        self.assertEqual(expected, deciphered)

    def test_2(self):
        cipher = "Yvzs! I xzm'g yvorvev Lzmxv olhg srh qly zg gsv xlolmb!!"
        expected = "Yeah! I can't believe Lance lost his job at the colony!!"

        deciphered = solution(cipher)
        self.assertEqual(expected, deciphered)

    def test_2_modified_last_letter(self):
        cipher = "Yvzs! I xzm'g yvorvev Lzmxv olhg srh qly zg gsv xlolmB!!"
        expected = "Yeah! I can't believe Lance lost his job at the colonB!!"

        deciphered = solution(cipher)
        self.assertEqual(expected, deciphered)

    def test_encryption_word(self):
        cipher = "vmxibkgrlm"
        expected = "encryption"

        deciphered = solution(cipher)
        self.assertEqual(expected, deciphered)

    def test_empty_cipher(self):
        cipher = ""
        expected = ""

        deciphered = solution(cipher)
        self.assertEqual(expected, deciphered)

    def test_all_punctuation(self):
        cipher = "!@#%$__--+.,"
        expected = cipher

        deciphered = solution(cipher)
        self.assertEqual(expected, deciphered)

    def test_all_caps(self):
        cipher = "THIS IS A CAPS TEST"
        expected = "THIS IS A CAPS TEST"

        deciphered = solution(cipher)
        self.assertEqual(expected, deciphered)

    def test_input_too_large(self):
        cipher = ""
        for i in range(0, 1000001):
            cipher += "a"

        expected = ""

        deciphered = solution(cipher)
        self.assertEqual(expected, deciphered)
