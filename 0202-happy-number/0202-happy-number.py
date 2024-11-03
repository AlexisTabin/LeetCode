class Solution:
    def isHappy(self, n: int) -> bool:
        seen_numbers = {n: 0}
        while n != 1:
            tmp = 0
            for c in str(n):
                tmp += int(c)**2
            if tmp in seen_numbers:
                return False
            else:
                seen_numbers[tmp] = n
            n = tmp
        return True
        