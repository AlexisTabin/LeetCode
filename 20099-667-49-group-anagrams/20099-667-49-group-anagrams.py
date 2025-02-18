class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        anagrams = {}
        result = []
        for word in strs:
            sorted_w = ''.join(sorted(word))
            if sorted_w not in anagrams:
                anagrams[sorted_w] = [word]
            else:
                anagrams[sorted_w].append(word)
        
        for key in anagrams:
            result.append(anagrams[key])

        return result