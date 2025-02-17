# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def values(self,root):
        nodes = []
        if root is None:
            return
        else:
            nodes.append(root.val)
            if root.left:
                nodes += self.values(root.left)
            if root.right:
                nodes += self.values(root.right)
        return nodes

    def getMinimumDifference(self, root: Optional[TreeNode]) -> int:
        nodes = list(self.values(root))
        nodes.sort()
        mindiff = float('inf')
        for i in range(len(nodes)-1):
            mindiff = min(mindiff, abs(nodes[i]-nodes[i+1]))
        return mindiff    

    def getMinimumDifferenceOld(self, root: Optional[TreeNode]) -> int:
        def getMinHelper(root, minimum):
            if root is None:
                return minimum
            if root.left:
                min_left = root.val - root.left.val
                minimum = min(min_left, minimum)
            if root.right:
                min_right = root.right.val - root.val
                minimum = min(min_right, minimum)
            return min(getMinHelper(root.left, minimum), getMinHelper(root.right, minimum))
        return getMinHelper(root, 999999)
            