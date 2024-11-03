import re

regex = re.compile('[^a-zA-Z0-9]')

class Solution:
    def isPalindrome(self, s: str) -> bool:
        s = regex.sub('', s).lower()
        start = 0
        end = len(s)-1
        middle = len(s) // 2
        while start < middle:
            if s[start] != s[end]:
                return False
            end -= 1
            start += 1
        return True