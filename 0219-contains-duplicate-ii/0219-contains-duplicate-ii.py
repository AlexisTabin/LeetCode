class Solution:
    def containsNearbyDuplicate(self, nums: List[int], k: int) -> bool:
        duplicate = {}
        for i, num in enumerate(nums):
            if num in duplicate:
                if abs(duplicate[num] - i) <= k:
                    return True
            duplicate[num] = i
            
        return False