class Solution:
    def strStr(self, haystack: str, needle: str) -> int:
        h_index = 0
        n_index = 0
        for curr_h_index in range(len(haystack)):
            while curr_h_index + h_index < len(haystack) and n_index < len(needle) and haystack[curr_h_index + h_index] == needle[n_index]:
                n_index += 1
                h_index += 1
                if n_index == len(needle):
                    return curr_h_index
            else:
                n_index = 0
                h_index = 0
        return -1