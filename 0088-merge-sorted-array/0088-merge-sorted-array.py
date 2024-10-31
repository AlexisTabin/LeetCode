class Solution:
    def merge(self, nums1: List[int], m: int, nums2: List[int], n: int) -> None:
        """
        Do not return anything, modify nums1 in-place instead.
        """
        for i, j in enumerate(range(m, m+n)):
            nums1[j] = nums2[i]
        nums1.sort(reverse=False)
        
                