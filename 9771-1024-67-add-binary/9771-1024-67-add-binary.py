class Solution:
    def addBinary(self, a: str, b: str) -> str:
        result = ""
        ret = 0
        a_ptr = len(a)-1
        b_ptr = len(b)-1
        while(a_ptr >= 0 or b_ptr >= 0 or ret > 0):
            if a_ptr < 0:
                a_val = 0
            else:
                a_val = int(a[a_ptr])
            if b_ptr < 0:
                b_val = 0
            else:
                b_val = int(b[b_ptr])
            
            if a_val + b_val + ret == 1:
                result = "1" + result
                ret = 0
            elif a_val + b_val + ret == 2:
                result = "0" + result
                ret = 1
            elif a_val + b_val + ret == 3:
                result = "1" + result
                ret = 1
            else:
                result = "0" + result
                ret = 0
            a_ptr -= 1
            b_ptr -= 1
        return result

