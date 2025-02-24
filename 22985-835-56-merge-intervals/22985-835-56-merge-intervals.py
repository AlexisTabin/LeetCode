class Solution:
    def merge(self, intervals: List[List[int]]) -> List[List[int]]:
        def are_overlapping(first, second):
            return first[-1] >= second[0]

        intervals.sort(key=lambda x: x[0])

        result = []
        for interval in intervals:
            if len(result) == 0:
                result.append(interval)
            else:
                if are_overlapping(result[-1], interval):
                    new_interval = [min(interval[0], result[-1][0]), max(interval[1], result[-1][1])]
                    result[-1] = new_interval
                else:
                    result.append(interval)
                
        return result