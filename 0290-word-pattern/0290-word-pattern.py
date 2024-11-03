class Solution:
    def wordPattern(self, pattern: str, s: str) -> bool:
        pattern_map = {}
        words = s.split(' ')
        if len(pattern) == len(words):
            for i, letter in enumerate(pattern):
                if letter in pattern_map:
                    if pattern_map[letter] != words[i]:
                        return False
                else:
                    if words[i] in pattern_map.values():
                        return False
                    else:
                        pattern_map[letter] = words[i]
            return True
        else:
            return False