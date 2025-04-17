class Solution:
    def decodeMessage(self, key: str, message: str) -> str:
        decoder = {' ': ' '}
        alphabet = "abcdefghijklmnopqrstuvwxyz"
        i = 0
        for letter in key:
            if letter not in decoder:
                decoder[letter] = alphabet[i]
                i += 1
        output = ''
        for letter in message:
            output += decoder[letter]
        return output
            