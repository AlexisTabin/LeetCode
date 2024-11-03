class Solution:
    def canConstruct(self, ransomNote: str, magazine: str) -> bool:
        available_letters = {letter: 0 for letter in magazine}
        for letter in magazine:
            available_letters[letter] += 1
        for letter in ransomNote:
            if letter in available_letters:
                available_letters[letter] -= 1
                if available_letters[letter] < 0:
                    return False
            else:
                return False
        return True