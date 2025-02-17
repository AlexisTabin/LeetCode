class Solution:
    def searchInsert(self, nums: List[int], target: int) -> int:
        def find_index(nums, start, end, target):
            if ((end - start) <= 1):
                if nums[start] == target:
                    return start
                elif nums[end] == target:
                    return end
                else:
                    if target < nums[start]:
                        return start
                    elif target < nums[end]:
                        return end
                    else:
                        if end == (len(nums) - 1):
                            return end + 1
                        else:
                            return end 
            else:
                middle = ((start + end) // 2)
                if nums[middle] >= target:
                    return find_index(nums, start, middle, target)
                else:
                    return find_index(nums, middle, end, target)
        return find_index(nums, 0, len(nums) - 1, target)
                