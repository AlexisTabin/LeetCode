# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def mergeTwoLists(self, list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:
        answer = ListNode()
        while list1 and list2:
            tmp = ListNode()
            if list1.val < list2.val :
                tmp.val = list1.val
                list1 = list1.next
            else :
                tmp.val = list2.val
                list2 = list2.next
            last_ans = answer
            while last_ans.next != None:
                last_ans = last_ans.next
            last_ans.next = tmp

        if list1 or list2:
            last_ans = answer
            while last_ans.next != None:
                last_ans = last_ans.next
            last_ans.next = list1 if list1 else list2

        return answer.next

        