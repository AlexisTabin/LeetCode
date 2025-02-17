class Solution:
    def majorityElement(self, nums: List[int]) -> int:
        curr = nums[0]
        count = 0 
        for num in nums:
            if num == curr:
                count += 1
            else:
                if count <= 0:
                    curr = num
                else:
                    count -= 1
            print(count)
        
        return curr