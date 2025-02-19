# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def rightSideView(self, root: Optional[TreeNode]) -> List[int]:
        result = []
        if root:
            nodes = [root]
            while nodes:
                values = [node.val for node in nodes if node]
                if values:
                    result.append(values[-1])
                    new_nodes = []
                    for node in nodes:
                        if node:
                            if node.left:
                                new_nodes.append(node.left)
                            if node.right:
                                new_nodes.append(node.right)
                print(new_nodes)
                nodes = new_nodes
        return result