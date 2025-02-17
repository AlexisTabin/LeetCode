class Solution:
    def hammingWeight(self, n: int) -> int:
        count = 0
        i = 0
        # Since we use only 31 bits
        # we could set i to 31 instead
        while(2**i < n):
            i += 1
        while(i >= 0):
            if 2**i <= n: 
                count += 1
                n = n - 2**i
            i -= 1
        return count
            

