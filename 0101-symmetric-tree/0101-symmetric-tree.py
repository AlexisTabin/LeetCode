# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def isSymmetric(self, root: Optional[TreeNode]) -> bool:
        def areLeavesEqual(left, right):
            if left is None:
                return right is None
            if right is None:
                return left is None
            return left.val == right.val and areLeavesEqual(left.left, right.right) and areLeavesEqual(left.right, right.left)
        return areLeavesEqual(root.left, root.right)