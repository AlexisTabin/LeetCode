class Solution:
    def romanToIntFirstTry(self, s: str) -> int:
        result = 0

        roman_map = {
            'I' : 1,
            'V' : 5,
            'X' : 10, 
            'L' : 50,
            'C' : 100,
            'D' : 500,
            'M' : 1000
        }

        substract_letters = 'IXC'
        substract_next_letter = {
            'I' : 'VX',
            'X' : 'LC',
            'C' : 'DM'
        }

        
        for index, letter in enumerate(s):
            if index != len(s)-1 and letter in substract_letters:
                next_letter = s[index + 1]
                if next_letter in substract_next_letter[letter]:
                    result -= roman_map[letter]
                else :
                    result += roman_map[letter]
            else :
                result += roman_map[letter]
        return result

    def romanToInt(self, s: str) -> int:
        result = 0

        roman_map = {
            'I' : 1,
            'V' : 5,
            'X' : 10, 
            'L' : 50,
            'C' : 100,
            'D' : 500,
            'M' : 1000
        }
        
        for index, letter in enumerate(s):
            if index < len(s)-1 and roman_map[s[index]] < roman_map[s[index + 1]]:
                result -= roman_map[letter]
            else :
                result += roman_map[letter]
                
        return result