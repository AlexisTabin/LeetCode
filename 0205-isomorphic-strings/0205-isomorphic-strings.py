class Solution:
    def isIsomorphic(self, s: str, t: str) -> bool:
        if len(s) == len(t):
            iso_map = {}
            for i, c in enumerate(s):
                if c in iso_map:
                    if iso_map[c] != t[i]:
                        return False
                else:
                    if t[i] in iso_map.values():
                        return False
                    iso_map[c] = t[i]
            return True
        else:
            return False
        