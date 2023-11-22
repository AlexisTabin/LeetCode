class Solution:
    def isValid(self, s: str) -> bool:
        l = len(s)
        opened = '[{('
        mapped = {']' : '[' ,
        '}' : '{',
        ')' : '('}

        LIFO = []
        for element in s:
            if element in opened:
                LIFO.append(element)
            else:
                try:
                    last = LIFO[-1]
                    if mapped[element] == last:
                        LIFO.pop()
                    else:
                        return not True
                except:
                    return False
                
               

        return len(LIFO) == 0