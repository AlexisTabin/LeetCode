# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def isSameTree(self, p: Optional[TreeNode], q: Optional[TreeNode]) -> bool:
        def helper(p,q):
            if not p and q :
                return False
            if p and not q:
                return False
            if p and q:
                if p.val == q.val:
                    return helper(p.left, q.left) and helper(p.right, q.right)
                else:
                    return False
            if not p and not q:
                return True
        return helper(p, q)
            
            