class Solution:
    def unequalTriplets(self, nums: List[int]) -> int:
        result = []
        for k in range(len(nums)):
            for j in range(k):
                for i in range(j):
                    if i >= j or j >= k:
                        pass
                    else:
                        are_pairwise_distincts = nums[i] != nums[j] and nums[k] != nums[j] and nums[i] != nums[k]
                        if are_pairwise_distincts:
                            result.append((i,j,k))
        return len(result)
