class Solution:
    def findCenter(self, edges: List[List[int]]) -> int:
        counter = {}
        goal = len(edges)
        for edge in edges:
            for i in range(2):
                if edge[i] in counter:
                    counter[edge[i]] += 1
                else:
                    counter[edge[i]] = 1

                if counter[edge[i]] == goal:
                    return edge[i]

        