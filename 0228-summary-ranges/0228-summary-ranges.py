class Solution:
    def summaryRanges(self, nums: List[int]) -> List[str]:
        if not nums:
            return []
        result = []
        prev_nb = nums[0]
        start = nums[0]
        
        for i, num in enumerate(nums):
            
            if i == 0:
                start = num
            else:
                
                if num - prev_nb != 1:
                    if start == prev_nb:
                        result.append(f'{start}')
                    else:
                        result.append(f'{start}->{prev_nb}')
                    start = num 
                    
            
            if i == len(nums) - 1:
                if num - prev_nb == 1:
                    result.append(f'{start}->{num}')
                else:
                    result.append(f'{num}')
                    
            prev_nb = num
                    
        return result
            