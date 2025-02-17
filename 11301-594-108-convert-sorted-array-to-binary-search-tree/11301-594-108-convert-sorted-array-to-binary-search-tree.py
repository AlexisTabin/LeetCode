# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def sortedArrayToBST(self, nums: List[int]) -> Optional[TreeNode]:
        def helper(nums):
            if len(nums) == 0:
                return None
            if len(nums) == 1:
                return TreeNode(nums[0], None, None)
            middle = len(nums) // 2
            return TreeNode(nums[middle], helper(nums[:middle]), helper(nums[middle+1:]))
        
        middle = len(nums) // 2
        bst = TreeNode(nums[middle], helper(nums[:middle]), helper(nums[middle+1:]))
        return bst