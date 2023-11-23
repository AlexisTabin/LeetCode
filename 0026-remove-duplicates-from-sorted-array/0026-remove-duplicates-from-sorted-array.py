class Solution:
    def removeDuplicatesFirstTry(self, nums: List[int]) -> int:
        answer = []
        items_to_pop = []
        for i, num in enumerate(nums):
            if num not in answer:
                answer.append(num)
            else :
                items_to_pop.append(i-len(items_to_pop))
        for i in items_to_pop:
            nums.pop(i)
        return len(answer)
    
    def removeDuplicates(self, nums: List[int]) -> int:
        last_unique = 1
        for index in range(1, len(nums)):
            if nums[index] != nums[index-1]:
                nums[last_unique] = nums[index]
                last_unique += 1
        return last_unique