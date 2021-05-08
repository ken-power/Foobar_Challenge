# Lance and Janice: Decoding encrypted messages using the Atbash Cipher

## The problem

With messages in this secret code, every lowercase letter `[a...z]` is replaced with the corresponding one in `[z...a]`, while every other character (including uppercase letters and punctuation) is left untouched.  That is, `'a'` becomes `'z'`, `'b'` becomes `'y'`, `'c'` becomes `'x'`, etc.  

For instance, the word `vmxibkgrlm`, when decoded, would become `encryption`.

## Solution
This is an example of the [Atbash Cipher](https://en.wikipedia.org/wiki/Atbash). The Atbash Cipher is a very simple substitution cipher that is sometimes called mirror code. It is believed to be the first cipher ever used. According to Wikipedia, Atbash is a monoalphabetic substitution cipher originally used to encrypt the Hebrew alphabet. 

To use Atbash, you simply reverse the alphabet, so `a` becomes `z`, `b` becomes `y` and so on. The name derives from the first, last, second, and second to last Hebrew letters (**A**leph–**T**aw–**B**et–**Sh**in).
It can be modified for use with any known writing system with a standard collating order. Due to the fact that there is only one way to perform this, the Atbash cipher provides no communications security, as it lacks any sort of key. 

## Implementation
The modern English alphabet is a Latin alphabet consisting of 26 letters, each having an upper- and lower-case form. The solution only needs to decipher lowercase letters. Anything else in the ciphertext remains unchanged. Given the decimal code for `a` is `97` in Unicode, and `z` is `122`, we can use that information to iterate over the ciphertext to determine if each character is in the range `[a...z]`, or `[97...122]`.

```python
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

```

## Unit Tests

These are the 2 test cases provided by Google. 

```text
Input:
solution.solution("wrw blf hvv ozhg mrtsg'h vkrhlwv?")
Output:
    did you see last night's episode?

Input:
solution.solution("Yvzs! I xzm'g yvorvev Lzmxv olhg srh qly zg gsv xlolmb!!")
Output:
    Yeah! I can't believe Lance lost his job at the colony!!

```
There are also a bunch of hidden tests that the code must pass, but they don't tell you what those tests are. This is the set of unit test I built up along the way.
```python
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

```

## References
* Wikipedia. [Atbash Cipher](https://en.wikipedia.org/wiki/Atbash).
* Boxentriq. [Atbash Cipher](https://www.boxentriq.com/code-breaking/cipher-identifier#atbash-cipher).
* Wikipedia. [The English alphabet](https://en.wikipedia.org/wiki/English_alphabet)
* Wikipedia. [ASCII - American Standard Code for Information Interchange](https://en.wikipedia.org/wiki/ASCII)
* Wikipedia. [List of Unicode characters](https://en.wikipedia.org/wiki/List_of_Unicode_characters)
* Hanging Hyena. [Atbash Cipher Decoder](https://www.hanginghyena.com/solvers_a/atbash-cipher-decoder) - useful for testing and debugging.
* Das, J.C. and De, D., 2017. [Atbash cipher design for secure nanocommunication using QCA](https://www.icevirtuallibrary.com/doi/abs/10.1680/jnaen.16.00001). Nanomaterials and Energy, 6(1), pp.36-47.
* Morkel, T. and Eloff, J.H.P., 2004. [Encryption techniques: a timeline approach](https://www.researchgate.net/profile/Tayana_Morkel/publication/267230842_ENCRYPTION_TECHNIQUES_A_TIMELINE_APPROACH_Author_and_co-author/links/55fa644108aeafc8ac38b24c.pdf). Information and Computer Security Architecture (ICSA) Research Group, University of Pretoria, 2.
* Steiner, R., 1996. [The two sons of Neriah and the two editions of Jeremiah in the light of two atbash code-words for Babylon](https://brill.com/view/journals/vt/46/1/article-p74_5.xml). Vetus Testamentum, 46(1), pp.74-84.
* Biswas, M.H., Ali, M.A., Rahman, M. and Sohel, M.M.K., 2019. [A systematic study on classical cryptographic cypher in order to design a smallest cipher](https://www.researchgate.net/profile/Md_Shamim_Biswas/publication/337918612_A_systematic_study_on_classical_cryptographic_cypher_in_order_to_design_a_smallest_cipher/links/5df362c9a6fdcc28371d3bb1/A-systematic-study-on-classical-cryptographic-cypher-in-order-to-design-a-smallest-cipher.pdf). Int. J. Sci. Res. Publ, 9(12), pp.507-11.