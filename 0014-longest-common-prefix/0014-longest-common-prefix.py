class Solution:
    def longestCommonPrefix(self, strs: List[str]) -> str:
        prefix = ""

        word_len = [len(w) for w in strs]
        min_len = min(word_len)

        for i in range(min_len):
            temp = strs[0][i]
            for word in strs:
                if word[i] != temp:
                    return prefix
            prefix += temp
        
        return prefix
            