import heapq
class Solution:
    def findKthLargest(self, nums: List[int], k: int) -> int:
        k_nums = nums[:k]
        heapq.heapify(k_nums)

        for num in nums[k:]:
            if num > k_nums[0]:
                heapq.heapreplace(k_nums, num)

        return k_nums[0]
