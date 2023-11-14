class Solution:
    def isPalindromeUsingString(self, x: int) -> bool:
        if x < 0:
            return False
        x_string = f"{x}"
        middle = len(x_string) / 2 - 1
        for index, letter in enumerate(x_string):
            if index <= middle:
                if x_string[index] != x_string[len(x_string)-1-index]:
                    return False
        return True
    
    def isPalindrome(self, x: int) -> bool:
        if x < 0:
            return False
        
        temp = x
        reversed = 0
        # we want to reverse x and then check if x == reversed
        while(temp > 0):
            digit = temp % 10
            reversed = reversed*10 + digit
            temp = temp // 10

        return x == reversed