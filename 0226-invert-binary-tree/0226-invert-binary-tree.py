# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def invertTree(self, root: Optional[TreeNode]) -> Optional[TreeNode]:
        def helperInvert(root):
            if root is None:
                return
            tmp = root.left
            root.left = root.right
            root.right = tmp
            helperInvert(root.left)
            helperInvert(root.right)
        helperInvert(root)
        return root