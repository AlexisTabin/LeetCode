class Solution:
    def isSubsequence(self, s: str, t: str) -> bool:
        if s == "":
            return True

        s_pt = 0
        t_pt = 0
        while(t_pt < len(t) and (s_pt < len(s))):
            if s[s_pt] == t[t_pt]:
                s_pt += 1
                t_pt += 1
                if s_pt == len(s):
                    return True
            else:
                t_pt += 1
        if s_pt != len(s):
            return False
