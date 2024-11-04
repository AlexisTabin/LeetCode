# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, x):
#         self.val = x
#         self.next = None

class Solution:
    def hasCycle(self, head: Optional[ListNode]) -> bool:
        if not head:
            return False
        head.seen = True
        while head.next is not None:
            head = head.next
            if hasattr(head, 'seen'):
                return True
            head.seen = True
        return False
        