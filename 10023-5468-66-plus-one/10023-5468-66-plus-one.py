class Solution:
    def plusOne(self, digits: List[int]) -> List[int]:
        increment = 1
        result = []
        for digit in reversed(digits):
            new_digit = digit + increment
            if new_digit > 9:
                new_digit = 0
                increment = 1
            else:
                increment = 0
            result = [new_digit] + result
        if increment == 1:
            result = [1] + result
        return result